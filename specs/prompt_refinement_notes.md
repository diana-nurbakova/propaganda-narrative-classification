# Prompt Refinement Notes for Agora EMNLP Revision

## Status: Code infrastructure is already in place

The `prompt_template.py` already has:
- ✅ P0/P1/P2 prompt level switching
- ✅ Helper functions for decision rules, BERTopic keywords, confused pairs, ToM blocks
- ✅ ToM Stage 1 analysis prompt (`create_tom_analysis_prompt`)
- ✅ ToM arbitration prompt (`create_tom_arbitration_prompt`)
- ✅ Disambiguation prompt (`create_disambiguation_prompt`)
- ✅ Data file loaders with graceful fallback

What's missing:
- ❌ Data file: `annotation_guideline_rules.json` → **NOW CREATED** (see output)
- ❌ Data file: `tom_taxonomy.json` → **NOW CREATED** (template, needs Didi's completion)
- ❌ Data file: `bertopic_keywords.json` → Awaiting BERTopic runs on Colab
- ❌ Prompt text refinements documented below

---

## 1. CRITICAL: Anti-Over-Prediction Instruction

### Problem
The main failure mode is over-prediction (too many labels). The current
prompts ask the model to find narratives but don't sufficiently discourage
over-labeling. The annotation guidelines' "actively promotes" rule is the
key missing constraint.

### Current (P0) narrative prompt preamble
```
You are an expert propaganda narrative analyst with extensive experience 
in identifying and classifying manipulative communication patterns.
Your task is to analyze the given text and identify which specific 
propaganda narratives are present.
```

### Proposed change (all levels)
Add after the role description, BEFORE the narrative list:

```python
prompt_template += (
    "You are an expert propaganda narrative analyst with extensive "
    "experience in identifying and classifying manipulative "
    "communication patterns.\n"
    "Your task is to analyze the given text and identify which "
    "specific propaganda narratives are ACTIVELY PROMOTED.\n\n"
    "CRITICAL: A narrative is present ONLY if the text actively "
    "promotes, presents, or advances it. Merely MENTIONING a topic "
    "is NOT sufficient. For example, an article that reports on "
    "climate fears without amplifying them should NOT be labelled "
    "'Amplifying Climate Fears'. Be conservative — it is better to "
    "miss a borderline narrative than to over-predict.\n\n"
)
```

This should go into P0 too (it's from the annotation guidelines and
improves the baseline). It addresses the core over-prediction problem.

### Where in code
`create_narrative_system_prompt()` line ~223-228
`create_subnarrative_system_prompt()` line ~335-339

---

## 2. General Principles Block (P1/P2)

### Current
The `_format_general_principles()` helper is already called at P1/P2.
The principles come from the JSON file. They look good.

### Refinement
Add one more principle to the JSON (already included in the created file):
"A narrative is present only if the text ACTIVELY PROMOTES or PRESENTS it 
— merely mentioning a topic is NOT sufficient for assigning the label."

This makes it explicit in the P1/P2 general principles block. For P0,
the instruction added in §1 above covers it.

---

## 3. Confused Pair Block Formatting

### Current
`_confused_pair_block()` produces:
```
## DISAMBIGUATION RULES FOR FREQUENTLY CONFUSED LABELS
- CONFUSION between [label A] and [label B]: decision rule text
```

### Refinement
The block should appear AFTER the narrative list but BEFORE the
instructions section. Currently it does (line 247). Good.

Consider adding a brief framing line:
```python
out = [
    "\n## DISAMBIGUATION RULES FOR FREQUENTLY CONFUSED LABELS",
    "The following pairs are known to be frequently confused. "
    "Apply the decision rules below when you identify either label.",
]
```

---

## 4. ToM Block Integration (P2)

### Current
`_format_tom_block()` prepends the ToM analysis at the top of the prompt.

### Refinement
The current format is good but the instruction at the end could be
more specific. Current:

```python
"When you classify, give extra weight to narratives that operate "
f"through the {mechanism or 'identified'} mechanism above. Do not "
"invent narratives that contradict the persuasive intent.\n\n"
```

Proposed:
```python
"When you classify, use this analysis as follows:\n"
f"1. Prioritise narratives that operate through the '{mechanism}' "
"mechanism identified above.\n"
"2. If a narrative contradicts the identified persuasive intent, "
"require STRONGER evidence before assigning it.\n"
"3. If two narratives are equally plausible, prefer the one whose "
"cognitive mechanism matches the analysis above.\n\n"
```

This gives the model more structured guidance on HOW to use the ToM
analysis rather than a vague "give extra weight."

---

## 5. ToM Stage 1 Prompt Refinement

### Current (`create_tom_analysis_prompt`, line 489)
The prompt is solid. Minor refinements:

### Proposed additions
After "Then choose ONE primary cognitive mechanism from this set:"
add:

```python
"Note: Many propaganda texts use multiple mechanisms. Choose the "
"PRIMARY one — the mechanism most central to the text's persuasive "
"strategy. If genuinely uncertain between two, prefer the one that "
"best explains what the text DOES TO the reader (not what the text "
"talks ABOUT).\n\n"
```

This addresses the distinction between topic and intent that is
central to our ToM contribution.

---

## 6. Narrative Prompt: Confidence Score Request

### Current
The output format requests narrative_name, evidence_quote, reasoning.

### Proposed addition
Add confidence to the JSON schema:

```json
{
  "narratives": [
    {
      "narrative_name": "string",
      "evidence_quote": "string",
      "reasoning": "string",
      "confidence": "high|medium|low"
    }
  ]
}
```

And add this instruction:
```
- For each narrative, rate your confidence: 'high' (strong, explicit 
  evidence), 'medium' (implicit but clear), or 'low' (borderline, 
  could be over-interpretation). Narratives rated 'low' should only 
  be included if the evidence is genuinely present.
```

This gives us the confidence signal we discussed (for analysis)
while also making the model more self-aware about borderline cases
(potentially reducing over-prediction).

---

## 7. Sub-Narrative Prompt: "Other" Handling

### Current
The "Other" sub-narrative is handled well with a detailed example.
The instructions for when to use/not use "Other" are clear.

### Potential issue
The current instruction says:
"DO include '...: Other' alongside specific subnarratives if there 
is distinct, leftover evidence supporting the parent narrative."

This may encourage over-prediction of "Other". Consider tightening:
"DO include '...: Other' alongside specific subnarratives ONLY if 
there is distinct, substantial evidence supporting the parent 
narrative that does NOT match ANY specific subnarrative definition."

The word "substantial" raises the threshold.

---

## 8. Sub-Narrative Prompt: Missing General Principles

### Current
The sub-narrative prompt at P1/P2 does NOT prepend general principles
(unlike the narrative prompt). The code only adds the ToM block.

### Proposed
Add the general principles block to the sub-narrative prompt too:
```python
if prompt_level != "P0":
    prompt_template += _format_general_principles(rules)
```

The "actively promotes" rule is just as important at the sub-narrative
level. Add after line 333 in current code.

---

## 9. Data Files Needed (Summary)

| File | Status | Action |
|---|---|---|
| `annotation_guideline_rules.json` | Created | Copy to `data/` directory |
| `tom_taxonomy.json` | Template created | Didi fills in TODO fields |
| `bertopic_keywords.json` | Not yet | Run BERTopic on Colab, output as JSON |

### `bertopic_keywords.json` expected format:
```json
{
  "EN": {
    "Blaming the war on others rather than the invader": ["sanctions", "provoked", "NATO", "expansion", "Minsk"],
    "Discrediting Ukraine": ["corrupt", "nazi", "puppet", "criminal", "illegitimate"],
    ...
  },
  "RU": {
    "Blaming the war on others rather than the invader": ["санкции", "провокация", "НАТО", ...],
    ...
  }
}
```

Keywords should be per-language, per-narrative, top-5 by c-TF-IDF.
For confused pairs, also compute CONTRASTIVE keywords (unique to each
side of the pair) and add them under a separate key or as annotations
in the annotation_guideline_rules.json.

---

## 10. Testing Strategy for Prompt Changes

### P0 → P0' (anti-over-prediction only)
Before testing P1/P2, test adding ONLY the "actively promotes"
instruction to P0. This is a single-sentence change that may
significantly reduce over-prediction without adding any cost.
Run on Llama, 2 languages, 5 runs. Compare against existing P0 results.

If P0' already improves significantly, that becomes the new baseline
for P1/P2 comparisons.

### P1 testing
Requires: `annotation_guideline_rules.json` (done) + 
`bertopic_keywords.json` (awaiting BERTopic runs).

Can test partial P1 (rules only, no keywords) immediately.

### P2 testing  
Requires: P1 files + `tom_taxonomy.json` (Didi fills in) +
ToM Stage 1 outputs (one Llama call per document, cached).

---

## 11. Prompt Length Concerns

Adding P1/P2 content increases prompt length. Rough estimates:

| Level | Added tokens (narrative prompt) | Cost impact |
|---|---|---|
| P0 | Baseline (~1500 tokens) | 1.0× |
| P0' | +50 tokens (anti-overpredict) | ~1.0× |
| P1 | +200-400 tokens (rules + keywords + confused pairs) | ~1.1-1.2× |
| P2 | +150-200 tokens (ToM block) on top of P1 | ~1.3× |

These are input token increases. Output tokens stay the same.
At DeepSeek pricing, input tokens are cheap (~$0.27/M tokens for
DeepSeek V3), so the cost impact is minimal.

The bigger concern is whether longer prompts degrade Llama 3.3 70B
performance (context window saturation). Monitor this in Phase 1.
