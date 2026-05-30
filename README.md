# Agora: Multi-Agent LLM Framework for Hierarchical Narrative Classification

A configurable framework for hierarchical multi-label classification of propaganda narratives using large language models. Implements the **Agora** multi-agent ensemble approach for multilingual narrative detection, developed for [SemEval-2025 Task 10](https://propaganda.math.unipd.it/semeval2025task10/index.html).

## Data Access

The datasets used in this work are provided by the organisers of **SemEval-2025 Task 10: Multilingual Characterization and Extraction of Narratives from Online News**. Due to licensing restrictions, we cannot redistribute the data. To obtain the datasets, please contact the task organisers directly:

> **SemEval-2025 Task 10**
> https://propaganda.math.unipd.it/semeval2025task10/index.html

Once obtained, extract the data into the `data/` directory following the structure described below. The taxonomy definition files (`narrative_definitions.csv`, `subnarrative_definitions.csv`, `taxonomy.json`) are included in this repository.

## Model Weights

The fine-tuned mDeBERTa v3 model weights (~1.1 GB) will be made available upon paper acceptance via Zenodo with a permanent DOI. During the review period, the weights can be downloaded from:

> **[Download model weights](https://e.pcloud.link/publink/show?code=kZ4k53ZIA8O37x6H6RchsQfFpUz08nffvb7)**

To use the pre-trained model, download and extract the weights into:

```text
models/microsoft/mdeberta-v3-base_narratives_classifier_hierarchical/
```

Alternatively, you can train the model from scratch using the pipeline described in the [mDeBERTa Baseline](#mdeberta-baseline-fine-tuned-transformer) section.

## Overview

The system classifies news articles into a two-level taxonomy of **narratives** and **subnarratives** across two propaganda domains:
- **URW** (Ukraine-Russia War): 11 narratives, 38 subnarratives
- **CC** (Climate Change): 10 narratives, 35 subnarratives

Supported languages: English (EN), Bulgarian (BG), Hindi (HI), Portuguese (PT), Russian (RU).

## Classification Methods

All methods use the same hierarchical prompting strategy (Level-First) and differ in their ensemble/validation approach.

### Baseline (Single Agent)

A single LLM agent classifies narratives and subnarratives without ensemble or validation.

- 1 narrative agent, 1 subnarrative agent, no validation
- Lowest cost, highest variance, prone to hallucination

### Actor-Critic (Validation Pipeline)

A classifier agent generates predictions, then a separate critic agent validates and refines them. Up to 2 retry cycles.

- 1 narrative agent, 1 subnarrative agent, validation enabled
- ~2x cost of baseline, reduces hallucination through self-correction

### Agora (Multi-Agent Ensemble)

Multiple independent agents classify the same document, then predictions are aggregated via voting.

- 3 narrative agents (default), 1 subnarrative agent, no validation
- Reduced variance through consensus; aggregation strategy controls precision/recall

```
                +--> Agent 1 --> Predictions --+
Document -------+--> Agent 2 --> Predictions --+--> Voting --> Final Predictions
                +--> Agent 3 --> Predictions --+
```

### Aggregation Strategies

Given N agents with prediction sets P_1, P_2, ..., P_N:

| Strategy | Formula | Behaviour |
|----------|---------|-----------|
| **Intersection** | P_1 ∩ P_2 ∩ ... ∩ P_N | Label included only if ALL agents agree. Highest precision, lowest recall. |
| **Majority** | {label \| count(label) > N/2} | Label included if >50% of agents agree. Balanced. |
| **Union** | P_1 ∪ P_2 ∪ ... ∪ P_N | Label included if ANY agent predicts it. Highest recall, lowest precision. |

The Agora method is configured via YAML as `agora` (intersection), `agora_majority`, or `agora_union`.

**Important**: Intersection aggregation requires all agents to return valid predictions. If any agent returns an empty set (e.g., due to parsing failure), the intersection is empty and the document is labelled "Other". This makes intersection unreliable for weaker models; use `majority` or `union` instead.

### Self-Consistency (sc_3)

A single-model Self-Consistency baseline that samples the same model `k=3` times at a non-zero temperature and aggregates the predictions. Conceptually similar to Agora but with a single model identity replicated across runs rather than three independent agents.

- 3 narrative samples, 1 subnarrative sample
- Aggregation strategy controls precision/recall, same as Agora
- Configured via YAML as `sc_3` (majority, default), `sc_3_intersection`, or `sc_3_union`
- Sampling temperature is set per config (typically 0.7 for sc_3 variants)

### mDeBERTa Baseline (Fine-tuned Transformer)

A fine-tuned [mDeBERTa v3 base](https://huggingface.co/microsoft/mdeberta-v3-base) model serving as a non-LLM baseline. Uses a **hierarchical multi-head architecture**: a shared DeBERTa encoder feeds into a parent (narrative) classification head and separate child (subnarrative) classification heads for each narrative.

- **Training data**: Unified annotations from all 5 languages (`data/all-texts-unified/unified-annotations.tsv`, 3,566 documents)
- **Architecture**: `MultiHeadDebertaForHierarchicalClassification` — one binary classifier per narrative, one multi-label head per narrative for its child subnarratives
- **Inference**: Parent heads predict narratives above a threshold; for each predicted narrative, the corresponding child head predicts subnarratives
- **Deterministic**: No temperature or seed variation — single run per language

```
                            +-- Parent Head --> Narrative predictions
Document --> DeBERTa v3 --> |
                            +-- Child Head (per narrative) --> Subnarrative predictions
```

**Pipeline** (`src/mDeberta/run_all_languages.py`):
1. **Preprocess** — tokenises training data, builds hierarchical label maps (`preprocess_dataset.py`)
2. **Train** — fine-tunes mDeBERTa with BCE loss, positive class weighting (`train_mdeberta.py`)
3. **Inference** — classifies dev set documents for all 5 languages (`run_inference.py`)
4. **Output** — writes results in experiment format compatible with the analysis pipeline

```bash
# Full pipeline (preprocess + train + inference)
python src/mDeberta/run_all_languages.py

# Inference only (requires trained model)
python src/mDeberta/run_all_languages.py --inference-only

# Custom classification threshold (default: 0.55)
python src/mDeberta/run_all_languages.py --threshold 0.3
```

## Prompt Engineering Variants

We evaluate five prompt levels, defined in `src/H3Prompting/prompt_template.py` as `PROMPT_LEVELS = ("P0", "P0'", "P0T", "P1", "P2")`. Each level adds further context to the narrative and subnarrative classification prompts.

| Level | Components | Purpose |
|-------|-----------|---------|
| **P0** | Original baseline prompt (definitions + examples only) | Reference point; no additional instructions |
| **P0'** (`p0prime`) | P0 + anti-over-prediction rule | Adds a CRITICAL RULE instructing the model that a narrative is present only if the text *actively promotes* it (mere mention is not sufficient). Measures the effect of conservative-prediction guidance. |
| **P0T** (`p0t`) | P0 + ToM Stage 1 analysis | Prepends a cached Theory-of-Mind analysis of the document. Isolates the effect of audience-modelling context independently of the conservative-prediction rule. |
| **P1** | P0' + annotation-guideline decision rules + BERTopic keywords + confused-pair disambiguation | Adds per-narrative decision rules extracted from the annotation guidelines, per-language BERTopic keywords for each narrative, and a confused-pair block listing pairs that are commonly mislabelled together. |
| **P2** | P1 + ToM Stage 1 analysis | Full prompt: combines the structured guideline context from P1 with the Theory-of-Mind analysis from P0T/P2. |

### Prompt Components

- **Theory-of-Mind (ToM) analysis** — a separate LLM call (`create_tom_analysis_prompt`) produces a Stage 1 analysis identifying the document's intended audience, beliefs the author takes for granted, and persuasive intent. Cached results are prepended at P0T and P2.
- **Annotation-guideline decision rules** — per-narrative and per-subnarrative rules extracted from the SemEval-2025 Task 10 annotation guidelines, exposed to the model alongside each label's definition.
- **BERTopic keywords** — per-language, per-narrative keyword sets surfaced from BERTopic topic modelling on the training corpus, attached to each narrative at P1/P2.
- **Confused-pair disambiguation** — pairs of narratives that are frequently confused (from the organisers' acknowledged confused pairs) are explicitly listed in the prompt with disambiguation guidance.
- **Disambiguation step** — an optional second-pass prompt (`create_disambiguation_prompt`) reasoning over confused pairs when the initial prediction triggers a known confusion.

### Method × Prompt-Level Variants

The full experimental matrix combines each classification method with each prompt level — config filenames encode this as `<method>_<prompt-level>_<model>_<lang>_t<temp>.yaml`. Example:

- `agora_p2_gpt5nano_en_t00.yaml` — Agora (3-agent intersection), P2 prompt, GPT-5 Nano, English, temperature 0.0
- `sc_3_p1_deepseek_ru_t00.yaml` — Self-Consistency (k=3), P1 prompt, DeepSeek, Russian, temperature 0.0
- `baseline_p0prime_hf_llama33_70b_bg_t00.yaml` — Single-agent baseline, P0' prompt, Llama 3.3 70B (HF), Bulgarian, temperature 0.0

## Backbone Models

The following LLM backends were used in our experiments:

| Config Key | Provider | Model | Notes |
|------------|----------|-------|-------|
| `gpt5nano` | OpenAI | `openai:gpt-5-nano` | Native structured output. 200K TPM rate limit requires `max_concurrency: 1`. |
| `deepseek` | DeepSeek | `deepseek:deepseek-chat` | Prompt-based JSON extraction. Most reliable model in our experiments. |
| `mistral` | Mistral AI | `mistral:mistral-large-latest` | Prompt-based JSON extraction. **Fuzzy label matching** enabled (threshold 70) because Mistral returns semantically equivalent but not exact label names. |
| `together_llama33_70b` | Together AI | `together_ai:meta-llama/Llama-3.3-70B-Instruct` | Prompt-based JSON extraction. **Fuzzy matching** enabled. Requires **JSON key normalisation** (`_normalize_json_keys`) because Llama returns `{"narratives": [...]}` instead of `{"subnarratives": [...]}` for subnarrative classification. |
| `hf_llama33_70b` | Hugging Face | `huggingface:meta-llama/Llama-3.3-70B-Instruct` | Same model as `together_llama33_70b` but served via Hugging Face Inference. **Fuzzy matching** enabled. Useful for budget-free batch runs via HF Pro. |
| `deepinfra` | DeepInfra | Llama 3.3 70B Instruct | Alternative serving for Llama 3.3 70B. Used for self-consistency × P1/P2 exploratory runs (see `run_sc_p1p2_deepinfra.ps1`). |
| `gemini` | Google | `google_genai:gemini-2.5-flash` | Native structured output. Prone to rate-limit crashes; `max_tokens` must be kept at 8192 (higher values cause reasoning timeouts). |

### Structured Output Handling

- **Native structured output** (OpenAI, Anthropic, Google): uses `with_structured_output()` for JSON mode / function calling.
- **Prompt-based fallback** (DeepSeek, Mistral, Together AI): appends a JSON schema to the system prompt and parses the response with regex-based extraction (`structured_output_helper.py`).
- When native structured output fails (e.g., rate limiting), the system automatically falls back to prompt-based extraction.

### Fuzzy Label Matching

Some models return labels that are semantically correct but don't match the taxonomy exactly (e.g., "Discrediting Ukrainian government" instead of "Discrediting Ukrainian government and officials and policies"). For these models, fuzzy matching via `rapidfuzz` maps model output to canonical taxonomy labels:

- Enabled for: Mistral, Together AI Llama
- Threshold: 70 (0-100 scale, using `token_set_ratio` scorer)
- Matching order: exact match -> simplified match (without category prefix) -> fuzzy match

## Experiment Parameters

### Standard Configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| Runs per config | 5 | Different random seeds per run |
| Temperatures | 0.0, 0.7 | 0.0 for deterministic, 0.7 for sampling |
| Languages | EN, BG, HI, PT, RU | Dev set used for evaluation |
| Narrative agents | 3 | For all Agora variants |
| Subnarrative agents | 1 | Single agent for subnarratives |
| Label cleaning | Enabled | Filters predictions to valid taxonomy labels |
| max_concurrency | 1-5 | Controls both node-level and document-level parallelism |

### Model-Specific Settings

| Model | max_tokens | max_concurrency | Fuzzy matching | Special handling |
|-------|-----------|-----------------|----------------|------------------|
| GPT-5-nano | 16384 | 1 | No | Native JSON mode |
| DeepSeek | 8192 | 5 | No | - |
| Mistral | 8192 | 3 | Yes (70) | - |
| Together Llama 3.3 70B | 8192 | 5 | Yes (70) | JSON key normalisation |
| Gemini 2.5 Flash | 8192 | 3 | No | Native JSON mode |

### Reproducibility

Each multi-run experiment generates deterministic seeds from a base seed (42):
```
seed_i = hash(base_seed + run_id) % 2^31
```
Seeds are recorded in `experiment_manifest.json` alongside timestamps and run status.

## Data Format

### Expected Directory Structure

```
data/
+-- taxonomy.json                         # Hierarchical label definitions (required)
+-- narrative_definitions.csv             # Narrative definitions and examples
+-- subnarrative_definitions.csv          # Subnarrative definitions and examples
|
+-- train/                                # Training set (with gold labels)
|   +-- EN/
|   |   +-- raw-documents/                # Text files (.txt)
|   |   +-- subtask-3-annotations.txt     # Gold: filename<TAB>narrative<TAB>subnarrative<TAB>justification
|   +-- BG/ HI/ PT/ RU/                  # Same structure
|
+-- dev-documents_4_December/             # Dev set (with gold labels - used for evaluation)
|   +-- EN/
|   |   +-- subtask-2-documents/          # Text files (.txt)
|   |   +-- subtask-3-dominant-narratives.txt  # Gold: filename<TAB>narrative<TAB>subnarrative
|   +-- BG/ HI/ PT/ RU/
|
+-- testset/                              # Test set (no gold labels)
    +-- EN/ BG/ HI/ PT/ RU/
        +-- subtask-2-documents/           # Text files only
```

### Annotation Format

**Train set** (4 columns, tab-separated):
```
EN_CC_100013.txt    CC: Criticism of climate movement    CC: ...: Ad hominem attacks on key activists    [justification]
```

**Dev set** (3 columns, tab-separated):
```
EN_UA_DEV_100012.txt    URW: Discrediting the West, Diplomacy    URW: ...: The West does not care about Ukraine
```

**Prediction output** (3 columns, tab-separated, semicolon-separated multi-labels):
```
EN_UA_DEV_100012.txt    URW: Discrediting the West;URW: Russia is the Victim    URW: ...: The West is weak;URW: ...: The West is russophobic
```

### Taxonomy Structure

Labels follow the format `Category: Narrative: Subnarrative`:
- Categories: `URW`, `CC`
- Narratives: e.g., `URW: Discrediting Ukraine`
- Subnarratives: e.g., `URW: Discrediting Ukraine: Ukraine is associated with nazism`

Documents classified as neither URW nor CC are labelled `Other`.

## Installation

### Prerequisites

- Python 3.10+
- API keys for at least one LLM provider

### Setup

```bash
git clone https://github.com/<your-username>/propaganda-narrative-classification.git
cd propaganda-narrative-classification

python -m venv .venv
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

pip install -r requirements.txt
```

### API Keys

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=...
MISTRAL_API_KEY=...
TOGETHER_API_KEY=...
GOOGLE_API_KEY=...
```

## Running Experiments

### Single Experiment

```bash
cd src/H3Prompting
python run_with_config.py --config ../../configs/experiments/generated/core/agora_majority_deepseek_en_t00.yaml
```

### Multi-Run Experiment (5 runs with different seeds)

```bash
python run_multi_experiment.py \
    --config ../../configs/experiments/generated/core/agora_majority_deepseek_en_t00.yaml \
    --n-runs 5 \
    --experiment-id "agora_majority_deepseek_en_t00" \
    --output-dir ../../results/experiments/agora_majority_deepseek_en_t00/ \
    --log
```

### Batch Experiments (PowerShell)

Model-specific experiment runners that auto-skip completed experiments:

```powershell
.\run_experiments_mistral.ps1              # All Mistral experiments
.\run_experiments_gpt5nano.ps1             # All GPT-5-nano experiments
.\run_experiments_together.ps1             # All Together AI Llama experiments
.\run_experiments_deepseek.ps1             # All DeepSeek experiments

# Regenerate configs before running:
.\run_experiments_mistral.ps1 -Generate

# Clean incomplete experiments first (GPT-5-nano only):
.\run_experiments_gpt5nano.ps1 -Clean
```

#### EMNLP Experiment Matrix

The full EMNLP matrix (5 languages × multiple methods × P0–P2 prompts) runs through per-model orchestrators:

```powershell
.\run_experiments_deepseek_emnlp.ps1       # DeepSeek across the full EMNLP matrix
.\run_experiments_gpt5nano_emnlp.ps1       # GPT-5-nano across the full EMNLP matrix
.\run_experiments_llama_emnlp.ps1          # Llama 3.3 70B (Together / HF) across the full matrix
```

#### Targeted Sweeps and Ablations

```powershell
.\run_ablation_majority_union.ps1          # Aggregation-strategy ablation (intersection vs majority vs union)
.\run_aggregation_sweep_gpt5nano.ps1       # Aggregation sweep on GPT-5-nano
.\run_experiments_p0t.ps1                  # P0T (ToM-only) variants
.\run_p1nc_p2nc_deepseek.ps1               # P1nc / P2nc variants on DeepSeek
.\run_p1nc_p2nc_gpt5nano.ps1               # P1nc / P2nc variants on GPT-5-nano
.\run_sc_p1p2_deepseek.ps1                 # Self-Consistency × P1/P2 on DeepSeek
.\run_sc_p1p2_gpt5nano.ps1                 # Self-Consistency × P1/P2 on GPT-5-nano
.\run_sc_p1p2_deepinfra.ps1                # Self-Consistency × P1/P2 on Llama via DeepInfra
.\run_experiments_mdeberta_originals.ps1   # mDeBERTa baseline restricted to original (non-augmented) texts
.\run_remaining_experiments.ps1            # Resume / fill-in incomplete experiments
```

#### Reproduction and Test-Set Workflow

```powershell
.\run_dev_replicate_original.ps1           # Reproduce original Agora setup on the dev set
.\run_testset_replicate_original.ps1       # Reproduce original setup on the held-out test set
.\run_testset_submission.ps1               # Generate primary test-set submission files
.\run_testset_submission_alternative.ps1   # Generate alternative test-set submission (offline re-aggregation)
```

The test-set submission scripts produce SemEval-formatted `.txt` files under `results/testset_submissions/`. Uploading to the SemEval evaluation server is handled by `scripts/submit_to_semeval.py` (requires `SEMEVAL_PASSCODE` env var).

### Generating Configs

```bash
cd configs/experiments
python generate_configs.py \
    --methods agora agora_majority agora_union actor_critic baseline \
    --models deepseek mistral gpt5nano together_llama33_70b \
    --temps 0.0 0.7 \
    --cost-tracking \
    --output-dir generated/core/

# List all available models and methods:
python generate_configs.py --list
```

## Results Structure

```
results/experiments/
+-- agora_majority_deepseek_en_t00/
|   +-- experiment_manifest.json        # Seeds, timestamps, run status
|   +-- base_config.yaml                # Copy of config used
|   +-- run_1/
|   |   +-- results.txt                 # Predictions (TSV)
|   |   +-- cost_metrics.json           # API call tracking
|   |   +-- fuzzy_matching.json         # Fuzzy match details (if enabled)
|   +-- run_2/ ... run_5/
```

## Analysis

### Evaluate Predictions Against Gold Labels

```bash
cd src/analysis
python evaluate_devset_predictions.py \
    --predictions ../../results/experiments/agora_majority_deepseek_en_t00/run_1/results.txt \
    --gold ../../data/dev-documents_4_December/EN/subtask-3-dominant-narratives.txt
```

### Statistical Significance Testing

```bash
python statistical_testing.py compare \
    --method-a-dir ../../results/experiments/agora_majority_deepseek_en_t00 \
    --method-a-name "Agora Majority" \
    --method-b-dir ../../results/experiments/baseline_deepseek_en_t00 \
    --method-b-name "Baseline" \
    --ground-truth ../../data/dev-documents_4_December/EN/subtask-3-dominant-narratives.txt \
    --output ../../results/analysis/agora_vs_baseline.json
```

### Comprehensive Experiment Report

```bash
cd src/analysis
python experiment_results_report.py \
    --experiments-dir ../../results/experiments/ \
    --output ../../results/analysis/experiment_summary.md \
    --json-output ../../results/analysis/experiment_summary.json
```

Auto-discovers all experiments (including mDeBERTa baseline), evaluates all runs against ground truth, and generates a Markdown report with:

- Per-language results tables (narrative and subnarrative F1 scores)
- Mean +/- std with bootstrap 95% confidence intervals across runs
- Cross-method and cross-model comparisons
- Pairwise significance tests (Wilcoxon + paired t-test)

### Ensemble Size Ablation Study

```bash
cd src/analysis
python ensemble_ablation_report.py \
    --experiments-dir ../../results/experiments/ \
    --output ../../results/analysis/ensemble_ablation.md

# Restrict to a specific temperature
python ensemble_ablation_report.py \
    --experiments-dir ../../results/experiments/ \
    --temps 0.7 \
    --output ../../results/analysis/ensemble_ablation_t07.md
```

Evaluates Agora experiments with varying numbers of agents (1, 3, 5, 7) on a single model and language, producing narrative- and subnarrative-level metrics with pairwise significance tests. Used to determine the optimal ensemble size for the multi-agent voting framework.

### Voting Failure Analysis

```bash
cd src/analysis
python voting_failure_analysis.py \
    --experiments-dir ../../results/experiments/ \
    --ground-truth-dir ../../data/dev-documents_4_December/ \
    --output ../../results/analysis/voting_failure_report.md
```

Diagnoses failure modes in multi-agent voting: per-document error classification (false positives, false negatives, "Other" inflation), cross-run consensus to identify systematic failures across seeds, cross-aggregation comparison (intersection vs majority vs union on the same model), and cross-model consensus to surface inherently hard documents. When vote-level data is available, also analyses unanimous-wrong votes, agreement entropy, and per-agent reliability.

### Dataset Statistics

```bash
cd src/analysis
python dataset_statistics.py --output ../../results/analysis/dataset_statistics.md
```

Generates train/dev/test statistics: article counts, narrative/subnarrative distributions, label density, and cross-split label coverage analysis.

### Data Exploration

```bash
cd src/analysis
python data_exploration.py --output-dir ../../results/analysis/data_exploration/
```

Generates narrative co-occurrence matrices, category balance (URW vs CC) across languages, and train vs dev distribution comparisons.

## Repository Structure

```
propaganda-narrative-classification/
+-- src/
|   +-- H3Prompting/                    # Core LLM classification pipeline
|   |   +-- run_with_config.py          # Main entry point
|   |   +-- run_multi_experiment.py     # Multi-run orchestration
|   |   +-- graph_builder.py            # LangGraph computation graph construction
|   |   +-- graph_nodes.py              # Classification, validation, aggregation nodes
|   |   +-- config_loader.py            # YAML config parser (ClassificationConfig)
|   |   +-- schema.py                   # Pydantic models for structured LLM output
|   |   +-- structured_output_helper.py # JSON extraction + key normalisation
|   |   +-- fuzzy_label_matcher.py      # Fuzzy matching for variant labels
|   |   +-- label_info.py              # Taxonomy loading and flattening
|   |   +-- prompt_template.py          # LLM prompt templates
|   |   +-- cost_tracker.py             # API call cost tracking
|   |   +-- retrieval_filter.py         # Embedding-based label filtering
|   +-- analysis/                       # Evaluation and analysis scripts
|   |   +-- experiment_results_report.py  # Comprehensive report: all experiments, bootstrap CI, significance tests
|   |   +-- evaluate_devset_predictions.py
|   |   +-- statistical_testing.py
|   |   +-- dataset_statistics.py       # Train/dev/test statistics and distributions
|   |   +-- variance_analysis.py
|   |   +-- data_exploration.py         # Narrative co-occurrence analysis
|   +-- mDeberta/                       # Fine-tuned mDeBERTa baseline
|   |   +-- multihead_deberta.py       # Hierarchical multi-head model architecture
|   |   +-- preprocess_dataset.py      # Tokenisation and label map generation
|   |   +-- train_mdeberta.py          # Training loop with BCE loss
|   |   +-- run_inference.py           # Single-language inference
|   |   +-- run_all_languages.py       # Full pipeline orchestrator (all languages)
+-- configs/experiments/                # Experiment config generation
|   +-- generate_configs.py             # Config generator
|   +-- generated/core/                 # Generated YAML configs
+-- data/                               # Taxonomy definitions included; documents require download (see Data Access)
+-- results/                            # Experiment outputs
+-- run_experiments_*.ps1               # PowerShell experiment runners
```

## Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | 0.3.27 | LLM orchestration |
| langgraph | 1.0.0a3 | Graph-based pipeline |
| langchain-openai | 0.3.33 | OpenAI provider |
| langchain-deepseek | 0.1.4 | DeepSeek provider |
| langchain-mistralai | 0.2.11 | Mistral provider |
| langchain-together | 0.3.1 | Together AI provider |
| langchain-google-genai | 2.1.10 | Google Gemini provider |
| pydantic | 2.11.7 | Structured output schemas |
| rapidfuzz | - | Fuzzy label matching |
| scipy | 1.15.3 | Statistical testing |
| scikit-learn | 1.7.0 | Evaluation metrics |

## Citation

```bibtex
@inproceedings{agora2025,
  title={Agora: Multi-Agent LLM Framework for Hierarchical Narrative Classification},
  author={Anonymous},
  booktitle={},
  year={2025}
}
```

## Acknowledgments

- SemEval-2025 Task 10 organisers for the dataset and evaluation framework
- LangChain/LangGraph for the graph-based pipeline infrastructure
