# =============================================================================
# EMNLP Phase 1: Llama 3.3 70B Experiments (Free via HuggingFace)
# =============================================================================
# Implements spec S11.2 -- Phase 1 experiment matrix on Llama 3.3 70B.
#
# Experiment ordering (spec S11.2):
#   #1  P0  baseline        -- Llama baseline (original SIGIR prompt)
#   #6  SC  baseline (k=3)  -- Self-Consistency (run first alongside #1)
#   #2  P0' baseline        -- Anti-over-prediction effect
#   #3  P1  baseline        -- Annotation rules + BERTopic keywords
#   #4  ToM Stage 1 cache   -- One call per doc (prerequisite for #5)
#   #5  P2  baseline        -- ToM chain (P1 + ToM analysis)
#   #7  Agora + best prompt -- Multi-agent consensus with winning prompt
#
# Usage:
#   .\run_experiments_llama_emnlp.ps1                  # Run all phases
#   .\run_experiments_llama_emnlp.ps1 -Phase 1         # Run only prompt comparison (#1,#2,#3)
#   .\run_experiments_llama_emnlp.ps1 -Phase 2         # Run SC baseline (#6)
#   .\run_experiments_llama_emnlp.ps1 -Phase 3         # Run ToM (#4,#5)
#   .\run_experiments_llama_emnlp.ps1 -Phase 4         # Run Agora + best (#7)
#   .\run_experiments_llama_emnlp.ps1 -Generate        # Regenerate configs first
#   .\run_experiments_llama_emnlp.ps1 -AnalysisOnly    # Skip experiments, run analysis
# =============================================================================

param(
    [int]$Phase = 0,         # 0 = all phases, 1-4 = specific phase
    [switch]$Generate,
    [switch]$AnalysisOnly,
    [switch]$Help
)

$ErrorActionPreference = "Stop"

# Load .env file if it exists
$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
    Write-Host "[Loading .env file...]"
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
            $parts = $line -split "=", 2
            $key = $parts[0].Trim()
            $value = $parts[1].Trim().Trim('"').Trim("'")
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
}

# Check for API key
if (-not $env:TOGETHER_API_KEY) {
    Write-Host "[ERROR] TOGETHER_API_KEY not set. Add it to .env or set as environment variable." -ForegroundColor Red
    Write-Host "  Get your key at: https://api.together.xyz/settings/api-keys"
    exit 1
}

# Detect Python
$Python = $null
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $Python = $venvPython
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $Python = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $Python = "python3"
} else {
    Write-Host "Error: Python not found. Please activate your virtual environment." -ForegroundColor Red
    exit 1
}

Write-Host "Using Python: $Python"

$NRuns = 5
$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/emnlp"
$ModelKey = "together_llama33_70b"
$Languages = @("en", "bg", "hi", "pt", "ru")

function Write-Phase($msg) {
    Write-Host ""
    Write-Host ("=" * 77) -ForegroundColor Cyan
    Write-Host "  $msg" -ForegroundColor Cyan
    Write-Host ("=" * 77) -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step($msg) {
    Write-Host "[EMNLP-LLAMA] $msg" -ForegroundColor Green
}

function Show-Usage {
    Write-Host "Usage: .\run_experiments_llama_emnlp.ps1 [-Phase N] [-Generate] [-AnalysisOnly] [-Help]"
    Write-Host ""
    Write-Host "EMNLP Phase 1: Llama 3.3 70B experiments (free via HuggingFace)."
    Write-Host ""
    Write-Host "Phases:"
    Write-Host "  1    Prompt comparison: P0 vs P0' vs P1 baselines (experiments #1, #2, #3)"
    Write-Host "  2    SC baseline: Self-Consistency k=3 with all voting strategies (#6)"
    Write-Host "  3    ToM: Stage 1 cache + P2 baseline (#4, #5)"
    Write-Host "  4    Agora: Multi-agent consensus with best prompt (#7)"
    Write-Host "  0    Run all phases sequentially (default)"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Generate      Regenerate config files before running"
    Write-Host "  -AnalysisOnly  Skip experiments, only run analysis on existing results"
    Write-Host "  -Help          Show this help message"
    Write-Host ""
    Write-Host "Environment:"
    Write-Host "  HF_TOKEN    HuggingFace API token (required)"
}

function Run-Experiment($config, $experimentId, $outputDir) {
    if (-not (Test-Path $config)) {
        Write-Host "[ERROR] Config not found: $config" -ForegroundColor Red
        return
    }

    if ((Test-Path $outputDir) -and (Test-Path "$outputDir/experiment_manifest.json")) {
        Write-Host "[SKIP] $experimentId already exists" -ForegroundColor Yellow
        return
    }

    Write-Step "Running: $experimentId ($NRuns runs)"
    & $Python src/H3Prompting/run_multi_experiment.py `
        --config $config `
        --n-runs $NRuns `
        --experiment-id $experimentId `
        --output-dir $outputDir `
        --log
}

# =============================================================================
# Config generation
# =============================================================================

if ($Help) {
    Show-Usage
    exit 0
}

# Methods needed for all EMNLP experiments
$AllMethods = @(
    "baseline",            # P0 (original SIGIR prompt)
    "baseline_p0prime",    # P0' (anti-over-prediction)
    "baseline_p1",         # P1 (rules + BERTopic)
    "baseline_p2",         # P2 (P1 + ToM)
    "sc_3",                # SC k=3 majority
    "sc_3_intersection",   # SC k=3 intersection
    "sc_3_union",          # SC k=3 union
    "agora",               # Agora 3-agent intersection (P0)
    "agora_p0prime",       # Agora + P0'
    "agora_majority",      # Agora 3-agent majority (P0)
    "agora_p1",            # Agora + P1
    "agora_p2"             # Agora + P2 (ToM)
)

$existingConfigs = Get-ChildItem "$ConfigDir/*${ModelKey}*" -ErrorAction SilentlyContinue
if ($Generate -or -not $existingConfigs) {
    Write-Phase "Generating EMNLP Llama 3.3 70B Configs"

    & $Python configs/experiments/generate_configs.py `
        --methods @AllMethods `
        --models $ModelKey `
        --temps 0.0 `
        --cost-tracking `
        --vote-saving `
        --output-dir $ConfigDir
}

if ($AnalysisOnly) {
    # Jump straight to analysis
    $Phase = 99
}

# =============================================================================
# PHASE 1: Prompt Comparison -- P0 vs P0' vs P1 baselines
# Spec experiments #1, #2, #3
# =============================================================================
if ($Phase -eq 0 -or $Phase -eq 1) {
    Write-Phase "PHASE 1: Prompt Comparison (P0 vs P0' vs P1)"

    # Experiment #1: P0 baseline (original SIGIR prompt)
    Write-Step "--- Experiment #1: P0 baseline ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/baseline_${ModelKey}_${lang}_t00.yaml" `
            "baseline_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/baseline_${ModelKey}_${lang}_t00/"
    }

    # Experiment #2: P0' baseline (anti-over-prediction)
    Write-Step "--- Experiment #2: P0' baseline ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/baseline_p0prime_${ModelKey}_${lang}_t00.yaml" `
            "baseline_p0prime_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/baseline_p0prime_${ModelKey}_${lang}_t00/"
    }

    # Experiment #3: P1 baseline (annotation rules + BERTopic)
    Write-Step "--- Experiment #3: P1 baseline ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/baseline_p1_${ModelKey}_${lang}_t00.yaml" `
            "baseline_p1_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/baseline_p1_${ModelKey}_${lang}_t00/"
    }

    Write-Step "Phase 1 complete. Quick comparison:"
    Write-Host "  Compare P0 vs P0' vs P1 to identify the winning prompt before Phase 3."
}

# =============================================================================
# PHASE 2: Self-Consistency Baseline (k=3)
# Spec experiment #6 -- run early to answer SIGIR reviewer question
# =============================================================================
if ($Phase -eq 0 -or $Phase -eq 2) {
    Write-Phase "PHASE 2: Self-Consistency Baseline (k=3)"

    # SC with majority voting (primary comparison with Agora)
    Write-Step "--- SC k=3 majority ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/sc_3_${ModelKey}_${lang}_t00.yaml" `
            "sc_3_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/sc_3_${ModelKey}_${lang}_t00/"
    }

    # SC with intersection voting
    Write-Step "--- SC k=3 intersection ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/sc_3_intersection_${ModelKey}_${lang}_t00.yaml" `
            "sc_3_intersection_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/sc_3_intersection_${ModelKey}_${lang}_t00/"
    }

    # SC with union voting
    Write-Step "--- SC k=3 union ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/sc_3_union_${ModelKey}_${lang}_t00.yaml" `
            "sc_3_union_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/sc_3_union_${ModelKey}_${lang}_t00/"
    }

    Write-Step "Phase 2 complete."
}

# =============================================================================
# PHASE 3: ToM -- Stage 1 cache + P2 baseline
# Spec experiments #4, #5
# =============================================================================
if ($Phase -eq 0 -or $Phase -eq 3) {
    Write-Phase "PHASE 3: ToM Reasoning Chain"

    # Experiment #5: P2 baseline (includes ToM Stage 1 automatically via config)
    # The pipeline runs ToM Stage 1 as part of P2 -- no separate caching step needed.
    Write-Step "--- Experiment #5: P2 baseline (ToM chain) ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/baseline_p2_${ModelKey}_${lang}_t00.yaml" `
            "baseline_p2_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/baseline_p2_${ModelKey}_${lang}_t00/"
    }

    Write-Step "Phase 3 complete."
}

# =============================================================================
# PHASE 4: Agora with best prompt
# Spec experiment #7 -- use P0' as default, run P1 too for comparison
# =============================================================================
if ($Phase -eq 0 -or $Phase -eq 4) {
    Write-Phase "PHASE 4: Agora Multi-Agent Consensus"

    # Agora with P0 (original, for comparison with SIGIR results)
    Write-Step "--- Agora + P0 (intersection) ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/agora_${ModelKey}_${lang}_t00.yaml" `
            "agora_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/agora_${ModelKey}_${lang}_t00/"
    }

    # Agora with P0' (anti-over-prediction)
    Write-Step "--- Agora + P0' (intersection) ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/agora_p0prime_${ModelKey}_${lang}_t00.yaml" `
            "agora_p0prime_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/agora_p0prime_${ModelKey}_${lang}_t00/"
    }

    # Agora majority with P0 (alternative voting)
    Write-Step "--- Agora + P0 (majority) ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/agora_majority_${ModelKey}_${lang}_t00.yaml" `
            "agora_majority_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/agora_majority_${ModelKey}_${lang}_t00/"
    }

    # Agora with P1
    Write-Step "--- Agora + P1 (intersection) ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/agora_p1_${ModelKey}_${lang}_t00.yaml" `
            "agora_p1_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/agora_p1_${ModelKey}_${lang}_t00/"
    }

    # Agora with P2 (ToM)
    Write-Step "--- Agora + P2 (intersection, ToM) ---"
    foreach ($lang in $Languages) {
        Run-Experiment `
            "$ConfigDir/agora_p2_${ModelKey}_${lang}_t00.yaml" `
            "agora_p2_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/agora_p2_${ModelKey}_${lang}_t00/"
    }

    Write-Step "Phase 4 complete."
}

# =============================================================================
# ANALYSIS: Run enhanced experiment report on all results
# =============================================================================
if ($Phase -eq 0 -or $Phase -eq 99) {
    Write-Phase "Running Enhanced Analysis (hF, HCR, TCM, Bootstrap CIs)"

    & $Python -m src.analysis.enhanced_experiment_report `
        --experiments-dir "$BaseOutputDir" `
        --ground-truth-dir "data/dev-documents_4_December/" `
        --output "results/analysis/emnlp_experiment_summary.md" `
        --json-output "results/analysis/emnlp_experiment_summary.json" `
        --tcm-output-dir "results/analysis/tcm/"

    Write-Step "Analysis complete. Results at:"
    Write-Host "  Markdown: results/analysis/emnlp_experiment_summary.md"
    Write-Host "  JSON:     results/analysis/emnlp_experiment_summary.json"
    Write-Host "  TCMs:     results/analysis/tcm/"
}

# =============================================================================
# Summary
# =============================================================================
Write-Phase "EMNLP Phase 1 (Llama 3.3 70B) -- Summary"

Write-Host "Experiment matrix (spec S11.2):" -ForegroundColor White
Write-Host ""
Write-Host "  PROMPT COMPARISON (Phase 1):" -ForegroundColor Yellow
Write-Host "    #1  baseline (P0)      -- 5 langs × 5 runs = 25 runs"
Write-Host "    #2  baseline_p0prime   -- 5 langs × 5 runs = 25 runs"
Write-Host "    #3  baseline_p1        -- 5 langs × 5 runs = 25 runs"
Write-Host ""
Write-Host "  SELF-CONSISTENCY (Phase 2):" -ForegroundColor Yellow
Write-Host "    #6a sc_3 (majority)    -- 5 langs × 5 runs = 25 runs"
Write-Host "    #6b sc_3_intersection  -- 5 langs × 5 runs = 25 runs"
Write-Host "    #6c sc_3_union         -- 5 langs × 5 runs = 25 runs"
Write-Host ""
Write-Host "  TOM CHAIN (Phase 3):" -ForegroundColor Yellow
Write-Host "    #5  baseline_p2 (ToM)  -- 5 langs × 5 runs = 25 runs"
Write-Host ""
Write-Host "  AGORA (Phase 4):" -ForegroundColor Yellow
Write-Host "    #7a agora (P0)         -- 5 langs × 5 runs = 25 runs"
Write-Host "    #7b agora_p0prime      -- 5 langs × 5 runs = 25 runs"
Write-Host "    #7c agora_majority     -- 5 langs × 5 runs = 25 runs"
Write-Host "    #7d agora_p1           -- 5 langs × 5 runs = 25 runs"
Write-Host "    #7e agora_p2 (ToM)     -- 5 langs × 5 runs = 25 runs"
Write-Host ""
Write-Host "  Total: ~275 runs, cost: EUR 0 (HuggingFace Pro)" -ForegroundColor Green
Write-Host ""

$completedExperiments = Get-ChildItem "$BaseOutputDir/*_${ModelKey}_*" -Directory -ErrorAction SilentlyContinue
if ($completedExperiments) {
    Write-Host "Completed experiments:" -ForegroundColor White
    $completedExperiments | ForEach-Object { Write-Host "  $($_.Name)" }
} else {
    Write-Host "No experiments completed yet." -ForegroundColor Yellow
}
