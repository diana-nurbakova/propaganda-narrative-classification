#!/usr/bin/env python3
"""
BERTopic keyword extraction for the SemEval-2025 narrative taxonomy.

Extracts the top-k keywords per narrative per language using the **training
set** documents (``data/all-texts-unified/``). Two extraction methods:

1. BERTopic (requires ``bertopic`` + ``sentence-transformers``) — clusters
   documents within each narrative and extracts c-TF-IDF keywords.
2. TF-IDF fallback — for narratives with < ``min_docs_bertopic`` documents,
   computes class-vs-rest TF-IDF keywords directly.

Output: ``data/bertopic_keywords.json`` consumed by ``prompt_template.py``
when ``prompt_level >= P1``.

Usage::

    python -m src.analysis.bertopic_keywords \\
        --annotations data/all-texts-unified/unified-annotations.tsv \\
        --texts-dir data/all-texts-unified/texts/ \\
        --output data/bertopic_keywords.json \\
        --top-k 10

Spec reference: ``specs/agora_emnlp_spec.md`` §9.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

# Soft-import heavy libs so we get a clear error message rather than ImportError
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    from bertopic import BERTopic
    BERTOPIC_AVAILABLE = True
except Exception:
    # Catches ImportError, AttributeError (numba/coverage clash), etc.
    BERTOPIC_AVAILABLE = False


# ---------------------------------------------------------------------------
# Multilingual stopwords
# ---------------------------------------------------------------------------

# NLTK language name mapping for our 5 languages
_LANG_TO_NLTK = {
    "EN": "english",
    "BG": "bulgarian",  # not in NLTK — handled by fallback below
    "HI": "hindi",      # not in NLTK — handled by fallback below
    "PT": "portuguese",
    "RU": "russian",
}

# Compact fallback stopword lists for languages missing from NLTK.
# Sources: ISO stopwords project, spaCy, Wikipedia frequency lists.
_BULGARIAN_STOPWORDS = {
    "а", "аз", "ако", "ала", "бе", "без", "беше", "би", "бил", "била",
    "били", "било", "бих", "бъда", "бъде", "бяха", "в", "вас", "ваш",
    "ваша", "вашите", "вашия", "вероятно", "вече", "ви", "вие", "винаги",
    "все", "всеки", "всички", "всичко", "всяка", "във", "върху", "г",
    "ги", "го", "година", "години", "да", "два", "двамата", "двата",
    "две", "до", "добре", "докато", "докога", "дори", "друг", "друга",
    "други", "е", "евентуално", "един", "една", "едни", "едно", "ето",
    "за", "зад", "заедно", "заради", "засега", "защо", "защото", "и",
    "из", "или", "им", "има", "иначе", "й", "каза", "как", "каква",
    "какво", "какъв", "като", "кога", "когато", "което", "които",
    "кой", "който", "колко", "която", "къде", "където", "към",
    "ли", "м", "ме", "между", "ми", "мен", "ми", "много", "мога",
    "могат", "може", "моля", "момента", "му", "н", "на", "над",
    "назад", "най", "нас", "наш", "наша", "нашата", "не", "нея",
    "ни", "ние", "никога", "нито", "но", "нов", "нова", "нови",
    "ново", "някой", "някъде", "няколко", "няма", "обаче", "около",
    "от", "отгоре", "отново", "още", "пак", "по", "повече",
    "повечето", "под", "поне", "поради", "после", "почти", "пред",
    "преди", "при", "пък", "първо", "с", "са", "само", "се", "сега",
    "си", "след", "сме", "со", "сред", "срещу", "сте", "съм", "със",
    "също", "т", "тази", "така", "такава", "такива", "такъв", "там",
    "твой", "те", "тези", "ти", "тия", "то", "това", "тогава", "този",
    "той", "толкова", "точно", "три", "трябва", "тук", "тъй", "тя",
    "тях", "у", "харесва", "ще", "щом", "я",
}

_HINDI_STOPWORDS = {
    "अंदर", "अत", "अपना", "अपनी", "अपने", "अभी", "आदि", "आप",
    "इत्यादि", "इन", "इनका", "इन्हीं", "इन्हें", "इन्होंने", "इस",
    "इसका", "इसकी", "इसके", "इसमें", "इसी", "इसे", "उन", "उनका",
    "उनकी", "उनके", "उनको", "उन्हीं", "उन्हें", "उन्होंने", "उस",
    "उसके", "उसी", "उसे", "एक", "एवं", "एस", "ऐसे", "और", "कई",
    "कर", "करता", "करते", "करना", "करने", "करें", "कहते", "कहा",
    "का", "काफ़ी", "कि", "कितना", "किन्हें", "किन्हों", "किया",
    "किर", "किस", "किसी", "किसे", "की", "कुछ", "कुल", "के", "को",
    "कोई", "कौन", "कौनसा", "गया", "घर", "जब", "जहाँ", "जा",
    "जितना", "जिन", "जिन्हें", "जिन्होंने", "जिस", "जिसे", "जीधर",
    "जैसा", "जैसे", "जो", "तक", "तब", "तरह", "तिन", "तिन्हें",
    "तिन्हों", "तिस", "तिसे", "तो", "था", "थी", "थे", "दबारा",
    "दिया", "दुसरा", "दूसरे", "दो", "द्वारा", "न", "नहीं", "ना",
    "निहायत", "नीचे", "ने", "पर", "पर", "पहले", "पूरा", "पे",
    "फिर", "बनी", "बही", "बहुत", "बाद", "बाला", "बिलकुल", "भी",
    "भीतर", "मगर", "मानो", "मे", "में", "यदि", "यह", "यहाँ", "यही",
    "या", "यिह", "ये", "रखें", "रहा", "रहे", "ऱ्विam", "लिए",
    "लिये", "लेकिन", "व", "वग़ैरह", "वर्ग", "वह", "वहाँ", "वहीं",
    "वाले", "वुह", "वे", "वो", "सकता", "सकते", "सबसे", "सभी",
    "साथ", "साबुत", "साभ", "सारा", "से", "सो", "ही", "हुआ", "हुई",
    "हुए", "है", "हैं", "हो", "होता", "होती", "होते", "होना", "होने",
}


def get_stopwords(language: Optional[str] = None) -> List[str]:
    """Return a combined stopword list: English + target language.

    Always includes English because many multilingual corpora mix in
    English tokens (URLs, proper nouns, boilerplate). Target-language
    stopwords are added on top.
    """
    words: set = set()

    # Try NLTK first
    try:
        import nltk
        nltk.download("stopwords", quiet=True)
        from nltk.corpus import stopwords as nltk_sw
        words.update(nltk_sw.words("english"))
        nltk_name = _LANG_TO_NLTK.get((language or "").upper(), "")
        if nltk_name and nltk_name in nltk_sw.fileids():
            words.update(nltk_sw.words(nltk_name))
    except Exception:
        # Minimal English fallback if NLTK is entirely unavailable
        words.update({
            "a", "an", "the", "and", "or", "but", "in", "on", "at", "to",
            "for", "of", "with", "by", "from", "is", "are", "was", "were",
            "be", "been", "being", "have", "has", "had", "do", "does",
            "did", "will", "would", "shall", "should", "may", "might",
            "can", "could", "not", "no", "nor", "so", "if", "then",
            "than", "too", "very", "just", "about", "up", "out", "that",
            "this", "these", "those", "it", "its", "he", "she", "they",
            "we", "you", "i", "me", "my", "your", "his", "her", "our",
            "their", "what", "which", "who", "whom", "how", "when",
            "where", "why", "all", "each", "every", "both", "few",
            "more", "most", "other", "some", "such", "only", "own",
            "same", "also", "as", "into", "over", "after", "before",
        })

    # Hardcoded fallbacks for BG and HI (not in NLTK)
    lang_upper = (language or "").upper()
    if lang_upper == "BG":
        words.update(_BULGARIAN_STOPWORDS)
    elif lang_upper == "HI":
        words.update(_HINDI_STOPWORDS)

    return sorted(words)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_annotations(annotations_path: str) -> List[Dict[str, Any]]:
    """Load TSV annotations. Each row: file_id \\t narratives \\t subnarratives."""
    rows = []
    with open(annotations_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            file_id = parts[0].strip()
            narrs = [n.strip() for n in parts[1].split(";") if n.strip() and n.strip().lower() != "other"]
            subs = [s.strip() for s in parts[2].split(";")] if len(parts) > 2 else []
            rows.append({"file_id": file_id, "narratives": narrs, "subnarratives": subs})
    return rows


def infer_language(file_id: str) -> Optional[str]:
    """Heuristic: language prefixed to file id, e.g. ``A6_CC_BG_*`` → BG,
    ``EN_ORIG_EN_*`` → EN, ``HI_CC_*`` → HI, etc."""
    parts = file_id.upper().split("_")
    langs = {"EN", "BG", "HI", "PT", "RU"}
    for p in parts[:3]:
        if p in langs:
            return p
    return None


def load_text(texts_dir: str, file_id: str) -> str:
    path = os.path.join(texts_dir, file_id)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def strip_domain_prefix(label: str) -> str:
    """``'URW: Discrediting Ukraine'`` → ``'Discrediting Ukraine'``."""
    m = re.match(r"^(URW|CC):\s*", label)
    if m:
        return label[m.end():]
    return label


# ---------------------------------------------------------------------------
# TF-IDF fallback
# ---------------------------------------------------------------------------

def tfidf_keywords(
    docs_by_class: Dict[str, List[str]],
    top_k: int = 10,
    language: Optional[str] = None,
) -> Dict[str, List[str]]:
    """For each class, compute class-vs-rest TF-IDF and return top-k terms.

    Uses multilingual stopwords (English + target language) so that
    high-frequency function words don't dominate the keyword lists.
    """
    if not SKLEARN_AVAILABLE:
        print("WARNING: sklearn not available, skipping TF-IDF keywords.")
        return {}
    sw = get_stopwords(language)
    all_classes = list(docs_by_class.keys())
    out: Dict[str, List[str]] = {}
    for cls in all_classes:
        pos_texts = docs_by_class[cls]
        neg_texts = []
        for other in all_classes:
            if other != cls:
                neg_texts.extend(docs_by_class[other])
        if not pos_texts:
            out[cls] = []
            continue
        corpus = pos_texts + neg_texts
        vectorizer = TfidfVectorizer(
            max_features=5000, stop_words=sw, min_df=2, max_df=0.9,
            sublinear_tf=True,
        )
        try:
            X = vectorizer.fit_transform(corpus)
        except Exception:
            out[cls] = []
            continue
        feature_names = vectorizer.get_feature_names_out()
        pos_tfidf = np.asarray(X[: len(pos_texts)].mean(axis=0)).flatten()
        neg_tfidf = np.asarray(X[len(pos_texts) :].mean(axis=0)).flatten()
        diff = pos_tfidf - neg_tfidf
        top_idx = diff.argsort()[::-1][:top_k]
        out[cls] = [str(feature_names[i]) for i in top_idx if diff[i] > 0]
    return out


# ---------------------------------------------------------------------------
# BERTopic extraction
# ---------------------------------------------------------------------------

def bertopic_keywords(
    docs_by_class: Dict[str, List[str]],
    top_k: int = 10,
    min_docs_bertopic: int = 10,
    embedding_model: str = "paraphrase-multilingual-mpnet-base-v2",
    language: Optional[str] = None,
) -> Dict[str, List[str]]:
    """Extract BERTopic c-TF-IDF keywords per narrative class.

    Uses multilingual stopwords (English + target language) for the
    internal c-TF-IDF vectoriser so that function words in any language
    are filtered out. Falls back to TF-IDF for classes with fewer than
    ``min_docs_bertopic`` documents.
    """
    if not BERTOPIC_AVAILABLE:
        print("WARNING: bertopic not available, using TF-IDF fallback for all classes.")
        return tfidf_keywords(docs_by_class, top_k, language=language)

    sw = get_stopwords(language)

    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer_model = CountVectorizer(
        stop_words=sw, ngram_range=(1, 2), min_df=2,
    )

    result: Dict[str, List[str]] = {}
    small_classes: Dict[str, List[str]] = {}

    for cls, docs in docs_by_class.items():
        if len(docs) < min_docs_bertopic:
            small_classes[cls] = docs
            continue
        try:
            model = BERTopic(
                embedding_model=embedding_model,
                vectorizer_model=vectorizer_model,
                nr_topics="auto",
                min_topic_size=max(3, len(docs) // 5),
                verbose=False,
            )
            topics, probs = model.fit_transform(docs)
            # Aggregate keywords across all topics by c-TF-IDF score
            kw_counts: Dict[str, float] = defaultdict(float)
            for tid in set(topics):
                if tid == -1:
                    continue
                topic_words = model.get_topic(tid)
                for word, score in topic_words[:top_k * 2]:
                    kw_counts[word] += score
            sorted_kw = sorted(kw_counts, key=kw_counts.get, reverse=True)
            result[cls] = sorted_kw[:top_k]
        except Exception as e:
            print(f"  BERTopic failed for {cls} ({len(docs)} docs): {e}")
            small_classes[cls] = docs

    # TF-IDF fallback for small / failed classes
    if small_classes:
        fallback = tfidf_keywords(small_classes, top_k, language=language)
        result.update(fallback)

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract per-language per-narrative BERTopic keywords."
    )
    parser.add_argument(
        "--annotations",
        default="data/all-texts-unified/unified-annotations.tsv",
    )
    parser.add_argument(
        "--texts-dir",
        default="data/all-texts-unified/texts/",
    )
    parser.add_argument(
        "--output",
        default="data/bertopic_keywords.json",
    )
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--min-docs-bertopic", type=int, default=10)
    parser.add_argument(
        "--embedding-model",
        default="paraphrase-multilingual-mpnet-base-v2",
    )
    args = parser.parse_args()

    rows = load_annotations(args.annotations)
    print(f"[bertopic] Loaded {len(rows)} annotation rows")

    # Group texts by (language, narrative) AND (language, subnarrative)
    narr_groups: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
    sub_groups: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
    # Cross-language aggregation pool for sparse sub-narratives
    sub_groups_all: Dict[str, List[str]] = defaultdict(list)
    n_texts = 0
    for r in rows:
        lang = infer_language(r["file_id"])
        if not lang:
            continue
        text = load_text(args.texts_dir, r["file_id"])
        if not text.strip():
            continue
        n_texts += 1
        for narr in r["narratives"]:
            bare = strip_domain_prefix(narr)
            narr_groups[lang][bare].append(text)
        for sub in r.get("subnarratives", []):
            if not sub or sub.strip().lower() in ("other", "none"):
                continue
            bare_sub = strip_domain_prefix(sub)
            sub_groups[lang][bare_sub].append(text)
            sub_groups_all[bare_sub].append(text)

    print(f"[bertopic] {n_texts} texts across {len(narr_groups)} languages")
    for lang in sorted(narr_groups):
        n_narr = len(narr_groups[lang])
        n_sub = len(sub_groups.get(lang, {}))
        print(f"  {lang}: {sum(len(v) for v in narr_groups[lang].values())} docs, "
              f"{n_narr} narratives, {n_sub} sub-narratives")

    # --- Narrative-level keywords ---
    result: Dict[str, Dict[str, List[str]]] = {}
    for lang in sorted(narr_groups):
        print(f"[bertopic] Processing narratives for {lang}...")
        result[lang] = bertopic_keywords(
            narr_groups[lang],
            top_k=args.top_k,
            min_docs_bertopic=args.min_docs_bertopic,
            embedding_model=args.embedding_model,
            language=lang,
        )
        n_kw = sum(len(v) for v in result[lang].values())
        print(f"  -> {n_kw} keywords across {len(result[lang])} narratives")

    # --- Sub-narrative-level keywords ---
    # Per spec §9.3: per-language when >=5 docs, cross-language for sparse ones
    MIN_DOCS_SUBNARR = 5
    for lang in sorted(sub_groups):
        print(f"[bertopic] Processing sub-narratives for {lang}...")
        lang_sub = sub_groups[lang]
        # Split into sufficient and sparse
        sufficient: Dict[str, List[str]] = {}
        sparse_keys: List[str] = []
        for sub_name, docs in lang_sub.items():
            if len(docs) >= MIN_DOCS_SUBNARR:
                sufficient[sub_name] = docs
            else:
                sparse_keys.append(sub_name)
        if sufficient:
            sub_kw = bertopic_keywords(
                sufficient,
                top_k=args.top_k,
                min_docs_bertopic=args.min_docs_bertopic,
                embedding_model=args.embedding_model,
                language=lang,
            )
            result[lang].update(sub_kw)
            print(f"  -> {sum(len(v) for v in sub_kw.values())} keywords across "
                  f"{len(sub_kw)} sub-narratives (per-language)")
        # Sparse sub-narratives: use cross-language pool
        if sparse_keys:
            sparse_docs = {k: sub_groups_all[k] for k in sparse_keys if sub_groups_all[k]}
            if sparse_docs:
                sparse_kw = tfidf_keywords(sparse_docs, args.top_k, language=lang)
                result[lang].update(sparse_kw)
                print(f"  -> {sum(len(v) for v in sparse_kw.values())} keywords across "
                      f"{len(sparse_kw)} sparse sub-narratives (cross-language TF-IDF)")

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[bertopic] Written to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
