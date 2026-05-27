# =============================================================================
# EMNLP: GPT-5 Nano Cross-Model Validation
# =============================================================================
# Cross-model validation on GPT-5 Nano (3rd model after Llama + DeepSeek).
# 3 runs per condition (paid model).
#
# Experiments:
#   - SC baseline (k=3, P0'), 5 langs
#   - Baseline P0', P1, P2, 5 langs
#   - Agora P0', P1, P2, 5 langs
#
# Usage:
#   .\run_experiments_gpt5nano_emnlp.ps1              # Run all
#   .\run_experiments_gpt5nano_emnlp.ps1 -Generate    # Regenerate configs
#   .\run_experiments_gpt5nano_emnlp.ps1 -Phase 1     # Prompt comparison only
#   .\run_experiments_gpt5nano_emnlp.ps1 -Phase 2     # SC baseline only
#   .\run_experiments_gpt5nano_emnlp.ps1 -Phase 3     # ToM (P2) only
#   .\run_experiments_gpt5nano_emnlp.ps1 -Phase 4     # Agora only
# =============================================================================

param(
    [int]$Phase = 0,
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
if (-not $env:OPENAI_API_KEY) {
    Write-Host "[ERROR] OPENAI_API_KEY not set. Add it to .env or set as environment variable." -ForegroundColor Red
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
    Write-Host "Error: Python not found." -ForegroundColor Red
    exit 1
}

Write-Host "Using Python: $Python"

$NRuns = 3
$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/emnlp"
$ModelKey = "gpt5nano"
$AllLanguages = @("en", "bg", "hi", "pt", "ru")
$P2Languages = @("en", "bg", "hi", "pt", "ru")  # All languages

function Write-Phase($msg) {
    Write-Host ""
    Write-Host ("=" * 77) -ForegroundColor Yellow
    Write-Host "  $msg" -ForegroundColor Yellow
    Write-Host ("=" * 77) -ForegroundColor Yellow
    Write-Host ""
}

function Write-Step($msg) {
    Write-Host "[EMNLP-GPT5NANO] $msg" -ForegroundColor Green
}

function Show-Usage {
    Write-Host "Usage: .\run_experiments_gpt5nano_emnlp.ps1 [-Phase N] [-Generate] [-AnalysisOnly] [-Help]"
    Write-Host ""
    Write-Host "EMNLP: GPT-5 Nano cross-model validation."
    Write-Host ""
    Write-Host "Phases:"
    Write-Host "  1    Prompt comparison: P0' vs P1 baselines"
    Write-Host "  2    SC baseline: k=3 with majority/intersection/union"
    Write-Host "  3    ToM: P2 baseline (EN, RU, HI only)"
    Write-Host "  4    Agora: multi-agent with P0', P1, P2"
    Write-Host "  0    Run all phases sequentially (default)"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Generate      Regenerate config files before running"
    Write-Host "  -AnalysisOnly  Skip experiments, only run analysis"
    Write-Host "  -Help          Show this help message"
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

if ($Help) {
    Show-Usage
    exit 0
}

# Generate configs
$Methods = @(
    "baseline_p0prime",
    "baseline_p1",
    "baseline_p2",
    "sc_3",
    "sc_3_intersection",
    "sc_3_union",
    "agora_p0prime",
    "agora_p1",
    "agora_p2"
)

$existingConfigs = Get-ChildItem "$ConfigDir/*${ModelKey}*" -ErrorAction SilentlyContinue
if ($Generate -or -not $existingConfigs) {
    Write-Phase "Generating EMNLP GPT-5 Nano Configs"

    & $Python configs/experiments/generate_configs.py `
        --methods @Methods `
        --models $ModelKey `
        --temps 0.0 `
        --cost-tracking `
        --vote-saving `
        --output-dir $ConfigDir
}

if ($AnalysisOnly) {
    $Phase = 99
}

# =============================================================================
# PHASE 1: Prompt Comparison -- P0' vs P1 baselines
# =============================================================================
if ($Phase -eq 0 -or $Phase -eq 1) {
    Write-Phase "PHASE 1: Prompt Comparison (P0' vs P1)"

    Write-Step "--- P0' baseline ---"
    foreach ($lang in $AllLanguages) {
        Run-Experiment `
            "$ConfigDir/baseline_p0prime_${ModelKey}_${lang}_t00.yaml" `
            "baseline_p0prime_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/baseline_p0prime_${ModelKey}_${lang}_t00/"
    }

    Write-Step "--- P1 baseline ---"
    foreach ($lang in $AllLanguages) {
        Run-Experiment `
            "$ConfigDir/baseline_p1_${ModelKey}_${lang}_t00.yaml" `
            "baseline_p1_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/baseline_p1_${ModelKey}_${lang}_t00/"
    }

    Write-Step "Phase 1 complete."
}

# =============================================================================
# PHASE 2: Self-Consistency Baseline (k=3)
# =============================================================================
if ($Phase -eq 0 -or $Phase -eq 2) {
    Write-Phase "PHASE 2: Self-Consistency Baseline (k=3)"

    Write-Step "--- SC k=3 majority ---"
    foreach ($lang in $AllLanguages) {
        Run-Experiment `
            "$ConfigDir/sc_3_${ModelKey}_${lang}_t00.yaml" `
            "sc_3_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/sc_3_${ModelKey}_${lang}_t00/"
    }

    Write-Step "--- SC k=3 intersection ---"
    foreach ($lang in $AllLanguages) {
        Run-Experiment `
            "$ConfigDir/sc_3_intersection_${ModelKey}_${lang}_t00.yaml" `
            "sc_3_intersection_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/sc_3_intersection_${ModelKey}_${lang}_t00/"
    }

    Write-Step "--- SC k=3 union ---"
    foreach ($lang in $AllLanguages) {
        Run-Experiment `
            "$ConfigDir/sc_3_union_${ModelKey}_${lang}_t00.yaml" `
            "sc_3_union_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/sc_3_union_${ModelKey}_${lang}_t00/"
    }

    Write-Step "Phase 2 complete."
}

# =============================================================================
# PHASE 3: ToM -- P2 baseline (subset of languages)
# =============================================================================
if ($Phase -eq 0 -or $Phase -eq 3) {
    Write-Phase "PHASE 3: P2 (ToM) on EN, RU, HI"

    foreach ($lang in $P2Languages) {
        Run-Experiment `
            "$ConfigDir/baseline_p2_${ModelKey}_${lang}_t00.yaml" `
            "baseline_p2_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/baseline_p2_${ModelKey}_${lang}_t00/"
    }

    Write-Step "Phase 3 complete."
}

# =============================================================================
# PHASE 4: Agora with P0', P1, P2
# =============================================================================
if ($Phase -eq 0 -or $Phase -eq 4) {
    Write-Phase "PHASE 4: Agora Multi-Agent Consensus"

    Write-Step "--- Agora + P0' ---"
    foreach ($lang in $AllLanguages) {
        Run-Experiment `
            "$ConfigDir/agora_p0prime_${ModelKey}_${lang}_t00.yaml" `
            "agora_p0prime_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/agora_p0prime_${ModelKey}_${lang}_t00/"
    }

    Write-Step "--- Agora + P1 ---"
    foreach ($lang in $AllLanguages) {
        Run-Experiment `
            "$ConfigDir/agora_p1_${ModelKey}_${lang}_t00.yaml" `
            "agora_p1_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/agora_p1_${ModelKey}_${lang}_t00/"
    }

    Write-Step "--- Agora + P2 (ToM) ---"
    foreach ($lang in $P2Languages) {
        Run-Experiment `
            "$ConfigDir/agora_p2_${ModelKey}_${lang}_t00.yaml" `
            "agora_p2_${ModelKey}_${lang}_t00" `
            "$BaseOutputDir/agora_p2_${ModelKey}_${lang}_t00/"
    }

    Write-Step "Phase 4 complete."
}

# =============================================================================
# ANALYSIS
# =============================================================================
if ($Phase -eq 0 -or $Phase -eq 99) {
    Write-Phase "Running Enhanced Analysis"

    & $Python -m src.analysis.enhanced_experiment_report `
        --experiments-dir "$BaseOutputDir" `
        --ground-truth-dir "data/dev-documents_4_December/" `
        --output "results/analysis/emnlp_experiment_summary.md" `
        --json-output "results/analysis/emnlp_experiment_summary.json" `
        --tcm-output-dir "results/analysis/tcm/"

    Write-Step "Analysis complete."
    Write-Host "  Results: results/analysis/emnlp_experiment_summary.md"
}

# =============================================================================
# Summary
# =============================================================================
Write-Phase "GPT-5 Nano EMNLP Experiments -- Summary"

Write-Host "  PHASE 1: P0' + P1 baselines, 5 langs x 3 runs = 30 runs"
Write-Host "  PHASE 2: SC k=3 (maj/inter/union), 5 langs x 3 runs = 45 runs"
Write-Host "  PHASE 3: P2 (ToM), 3 langs x 3 runs = 9 runs"
Write-Host "  PHASE 4: Agora P0'/P1 (5 langs) + P2 (3 langs), 3 runs = 39 runs"
Write-Host ""
Write-Host "  Total: ~123 runs" -ForegroundColor Green
Write-Host ""

$completedExperiments = Get-ChildItem "$BaseOutputDir/*_${ModelKey}_*" -Directory -ErrorAction SilentlyContinue
if ($completedExperiments) {
    Write-Host "Completed experiments:" -ForegroundColor White
    $completedExperiments | ForEach-Object { Write-Host "  $($_.Name)" }
} else {
    Write-Host "No experiments completed yet." -ForegroundColor Yellow
}
