# =============================================================================
# Mistral Large Experiments (PowerShell)
# =============================================================================
# Run experiments with Mistral Large API model
# Note: Mistral uses fuzzy label matching to handle variant label outputs
#
# Usage:
#   .\run_experiments_mistral.ps1              # Run all Mistral experiments
#   .\run_experiments_mistral.ps1 -Generate    # Regenerate configs first
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
$ConfigDir = "configs/experiments/generated/core"

function Write-Phase($msg) {
    Write-Host ""
    Write-Host ("=" * 77) -ForegroundColor Blue
    Write-Host "  $msg" -ForegroundColor Blue
    Write-Host ("=" * 77) -ForegroundColor Blue
    Write-Host ""
}

function Write-Step($msg) {
    Write-Host "[MISTRAL] $msg" -ForegroundColor Green
}

function Show-Usage {
    Write-Host "Usage: .\run_experiments_mistral.ps1 [-Generate] [-Help]"
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

    Write-Step "Running: $experimentId"
    & $Python src/H3Prompting/run_multi_experiment.py `
        --config $config `
        --n-runs $NRuns `
        --experiment-id $experimentId `
        --output-dir $outputDir `
        --log
}

# =============================================================================
# Main
# =============================================================================

if ($Help) {
    Show-Usage
    exit 0
}

# Generate configs if requested or missing
$mistralConfigs = Get-ChildItem "$ConfigDir/*mistral*" -ErrorAction SilentlyContinue
if ($Generate -or -not $mistralConfigs) {
    Write-Phase "Generating Mistral Configs (with fuzzy matching)"

    & $Python configs/experiments/generate_configs.py `
        --methods agora agora_majority agora_union actor_critic baseline `
        --models mistral `
        --temps 0.0 0.7 `
        --cost-tracking `
        --output-dir $ConfigDir
}

# =============================================================================
# Core Method Comparison (EN, temp=0.0)
# =============================================================================
Write-Phase "Mistral: Core Methods (EN, temp=0.0)"

foreach ($method in @("agora", "agora_majority", "agora_union", "actor_critic", "baseline")) {
    Run-Experiment `
        "$ConfigDir/${method}_mistral_en_t00.yaml" `
        "${method}_mistral_en_t00" `
        "$BaseOutputDir/${method}_mistral_en_t00/"
}

# =============================================================================
# Temperature Comparison (EN, temp=0.7)
# =============================================================================
Write-Phase "Mistral: Temperature Comparison (EN, temp=0.7)"

foreach ($method in @("agora", "agora_majority", "agora_union", "actor_critic", "baseline")) {
    Run-Experiment `
        "$ConfigDir/${method}_mistral_en_t07.yaml" `
        "${method}_mistral_en_t07" `
        "$BaseOutputDir/${method}_mistral_en_t07/"
}

# =============================================================================
# Language Generalization (all methods across languages, temp=0.0)
# =============================================================================
Write-Phase "Mistral: Language Generalization"

foreach ($method in @("agora_majority", "actor_critic", "baseline")) {
    foreach ($lang in @("bg", "hi", "pt", "ru")) {
        Run-Experiment `
            "$ConfigDir/${method}_mistral_${lang}_t00.yaml" `
            "${method}_mistral_${lang}_t00" `
            "$BaseOutputDir/${method}_mistral_${lang}_t00/"
    }
}

# =============================================================================
# Complete
# =============================================================================
Write-Phase "Mistral Experiments Complete"

Write-Host "Results saved to: $BaseOutputDir/*_mistral_*"
Write-Host ""
Write-Host "Experiments completed:"
Get-ChildItem "$BaseOutputDir/*_mistral_*" -Directory -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  $_" }
