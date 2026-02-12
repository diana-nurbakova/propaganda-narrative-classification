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

## Backbone Models

The following LLM backends were used in our experiments:

| Config Key | Provider | Model | Notes |
|------------|----------|-------|-------|
| `gpt5nano` | OpenAI | `openai:gpt-5-nano` | Native structured output. 200K TPM rate limit requires `max_concurrency: 1`. |
| `deepseek` | DeepSeek | `deepseek:deepseek-chat` | Prompt-based JSON extraction. Most reliable model in our experiments. |
| `mistral` | Mistral AI | `mistral:mistral-large-latest` | Prompt-based JSON extraction. **Fuzzy label matching** enabled (threshold 70) because Mistral returns semantically equivalent but not exact label names. |
| `together_llama33_70b` | Together AI | `together_ai:meta-llama/Llama-3.3-70B-Instruct` | Prompt-based JSON extraction. **Fuzzy matching** enabled. Requires **JSON key normalisation** (`_normalize_json_keys`) because Llama returns `{"narratives": [...]}` instead of `{"subnarratives": [...]}` for subnarrative classification. |
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

# Regenerate configs before running:
.\run_experiments_mistral.ps1 -Generate

# Clean incomplete experiments first (GPT-5-nano only):
.\run_experiments_gpt5nano.ps1 -Clean
```

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
