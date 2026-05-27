# =============================================================================
# EMNLP Phase 2: DeepSeek Confirmation (~EUR 40)
# =============================================================================
# Implements spec S11.3 -- Phase 2 cross-model validation on DeepSeek.
# Run AFTER Phase 1 (Llama) to confirm findings on a paid model.
#
# Experiment ordering (spec S11.3):
#   #8   SC baseline (k=3) on DeepSeek, P0', 5 langs, 3 runs
#   #9   Best prompt, single-agent, 5 langs, 3 runs
#   #10  Best prompt + Agora (k=3), 5 langs, 3 runs
#   #11  P2 single-agent, 3 langs (EN, RU, HI), 3 runs
#   #12  ToM Stage 1 cache (100 docs), 1 run
#
# Usage:
#   .\run_experiments_deepseek_emnlp.ps1              # Run all
#   .\run_experiments_deepseek_emnlp.ps1 -Generate    # Regenerate configs
# =============================================================================

param(
    [switch]$Generate,
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
if (-not $env:DEEPSEEK_API_KEY) {
    Write-Host "[ERROR] DEEPSEEK_API_KEY not set. Add it to .env or set as environment variable." -ForegroundColor Red
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

$NRuns = 3  # Fewer runs for paid model (sufficient for mean + CI)
$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/emnlp"
$ModelKey = "deepseek"
$AllLanguages = @("en", "bg", "hi", "pt", "ru")
$P2Languages = @("en", "bg", "hi", "pt", "ru")  # All languages

function Write-Phase($msg) {
    Write-Host ""
    Write-Host ("=" * 77) -ForegroundColor Magenta
    Write-Host "  $msg" -ForegroundColor Magenta
    Write-Host ("=" * 77) -ForegroundColor Magenta
    Write-Host ""
}

function Write-Step($msg) {
    Write-Host "[EMNLP-DEEPSEEK] $msg" -ForegroundColor Green
}

function Show-Usage {
    Write-Host "Usage: .\run_experiments_deepseek_emnlp.ps1 [-Generate] [-Help]"
    Write-Host ""
    Write-Host "EMNLP Phase 2: DeepSeek cross-model validation (~EUR 40)."
    Write-Host "Run AFTER Phase 1 (Llama) results are analysed."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Generate    Regenerate config files before running"
    Write-Host "  -Help        Show this help message"
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
    "baseline_p0prime",    # Best prompt baseline (P0')
    "baseline_p1",         # P1 baseline
    "baseline_p2",         # P2 (ToM)
    "sc_3",                # SC k=3 majority
    "agora_p0prime",       # Agora + P0'
    "agora_p1"             # Agora + P1
)

$existingConfigs = Get-ChildItem "$ConfigDir/*${ModelKey}*" -ErrorAction SilentlyContinue
if ($Generate -or -not $existingConfigs) {
    Write-Phase "Generating EMNLP DeepSeek Configs"

    & $Python configs/experiments/generate_configs.py `
        --methods @Methods `
        --models $ModelKey `
        --temps 0.0 `
        --cost-tracking `
        --vote-saving `
        --output-dir $ConfigDir
}

# =============================================================================
# Experiment #8: SC baseline on DeepSeek
# =============================================================================
Write-Phase "Experiment #8: SC Baseline (k=3, DeepSeek)"

foreach ($lang in $AllLanguages) {
    Run-Experiment `
        "$ConfigDir/sc_3_${ModelKey}_${lang}_t00.yaml" `
        "sc_3_${ModelKey}_${lang}_t00" `
        "$BaseOutputDir/sc_3_${ModelKey}_${lang}_t00/"
}

# =============================================================================
# Experiment #9: Best prompt, single-agent
# Using P0' as the likely best (adjust after Phase 1 analysis)
# =============================================================================
Write-Phase "Experiment #9: Best Prompt Single-Agent (DeepSeek)"

foreach ($lang in $AllLanguages) {
    Run-Experiment `
        "$ConfigDir/baseline_p0prime_${ModelKey}_${lang}_t00.yaml" `
        "baseline_p0prime_${ModelKey}_${lang}_t00" `
        "$BaseOutputDir/baseline_p0prime_${ModelKey}_${lang}_t00/"
}

# Also run P1 for comparison
foreach ($lang in $AllLanguages) {
    Run-Experiment `
        "$ConfigDir/baseline_p1_${ModelKey}_${lang}_t00.yaml" `
        "baseline_p1_${ModelKey}_${lang}_t00" `
        "$BaseOutputDir/baseline_p1_${ModelKey}_${lang}_t00/"
}

# =============================================================================
# Experiment #10: Best prompt + Agora
# =============================================================================
Write-Phase "Experiment #10: Agora + Best Prompt (DeepSeek)"

foreach ($lang in $AllLanguages) {
    Run-Experiment `
        "$ConfigDir/agora_p0prime_${ModelKey}_${lang}_t00.yaml" `
        "agora_p0prime_${ModelKey}_${lang}_t00" `
        "$BaseOutputDir/agora_p0prime_${ModelKey}_${lang}_t00/"
}

# =============================================================================
# Experiment #11: P2 (ToM) on subset of languages
# =============================================================================
Write-Phase "Experiment #11: P2 (ToM) on EN, RU, HI (DeepSeek)"

foreach ($lang in $P2Languages) {
    Run-Experiment `
        "$ConfigDir/baseline_p2_${ModelKey}_${lang}_t00.yaml" `
        "baseline_p2_${ModelKey}_${lang}_t00" `
        "$BaseOutputDir/baseline_p2_${ModelKey}_${lang}_t00/"
}

# =============================================================================
# Analysis
# =============================================================================
Write-Phase "Running Enhanced Analysis"

& $Python -m src.analysis.enhanced_experiment_report `
    --experiments-dir "$BaseOutputDir" `
    --ground-truth-dir "data/dev-documents_4_December/" `
    --output "results/analysis/emnlp_experiment_summary.md" `
    --json-output "results/analysis/emnlp_experiment_summary.json" `
    --tcm-output-dir "results/analysis/tcm/"

Write-Phase "EMNLP Phase 2 (DeepSeek) Complete"
Write-Host "Estimated cost: ~EUR 40" -ForegroundColor Yellow
Write-Host "Results: results/analysis/emnlp_experiment_summary.md"
