# =============================================================================
# Together AI Llama Experiments (PowerShell)
# =============================================================================
# Run experiments with Llama 3.3 70B via Together AI API
# Requires: pip install langchain-together
# Set TOGETHER_API_KEY in .env or environment
#
# Usage:
#   .\run_experiments_together.ps1              # Run all experiments
#   .\run_experiments_together.ps1 -Generate    # Regenerate configs first
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
$ConfigDir = "configs/experiments/generated/core"
$ModelKey = "together_llama33_70b"

function Write-Phase($msg) {
    Write-Host ""
    Write-Host ("=" * 77) -ForegroundColor Blue
    Write-Host "  $msg" -ForegroundColor Blue
    Write-Host ("=" * 77) -ForegroundColor Blue
    Write-Host ""
}

function Write-Step($msg) {
    Write-Host "[TOGETHER] $msg" -ForegroundColor Green
}

function Show-Usage {
    Write-Host "Usage: .\run_experiments_together.ps1 [-Generate] [-Help]"
    Write-Host ""
    Write-Host "Runs Llama 3.3 70B experiments via Together AI API."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Generate    Regenerate config files before running"
    Write-Host "  -Help        Show this help message"
    Write-Host ""
    Write-Host "Environment:"
    Write-Host "  TOGETHER_API_KEY    Together AI API key (required)"
    Write-Host "  https://api.together.xyz/settings/api-keys"
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
$togetherConfigs = Get-ChildItem "$ConfigDir/*${ModelKey}*" -ErrorAction SilentlyContinue
if ($Generate -or -not $togetherConfigs) {
    Write-Phase "Generating Together AI Llama 3.3 70B Configs"

    & $Python configs/experiments/generate_configs.py `
        --methods agora agora_majority agora_union actor_critic baseline `
        --models $ModelKey `
        --temps 0.0 0.7 `
        --cost-tracking `
        --output-dir $ConfigDir
}

# =============================================================================
# Core Method Comparison (EN, temp=0.0)
# =============================================================================
Write-Phase "Llama 3.3 70B: Core Methods (EN, temp=0.0)"

foreach ($method in @("agora", "agora_majority", "agora_union", "actor_critic", "baseline")) {
    Run-Experiment `
        "$ConfigDir/${method}_${ModelKey}_en_t00.yaml" `
        "${method}_${ModelKey}_en_t00" `
        "$BaseOutputDir/${method}_${ModelKey}_en_t00/"
}

# =============================================================================
# Temperature Comparison (EN, temp=0.7)
# =============================================================================
Write-Phase "Llama 3.3 70B: Temperature Comparison (EN, temp=0.7)"

foreach ($method in @("agora", "agora_majority", "agora_union", "actor_critic", "baseline")) {
    Run-Experiment `
        "$ConfigDir/${method}_${ModelKey}_en_t07.yaml" `
        "${method}_${ModelKey}_en_t07" `
        "$BaseOutputDir/${method}_${ModelKey}_en_t07/"
}

# =============================================================================
# Language Generalization (agora_majority across languages)
# =============================================================================
Write-Phase "Llama 3.3 70B: Language Generalization"

$bestMethod = "agora_majority"

foreach ($lang in @("bg", "hi", "pt", "ru")) {
    Run-Experiment `
        "$ConfigDir/${bestMethod}_${ModelKey}_${lang}_t00.yaml" `
        "${bestMethod}_${ModelKey}_${lang}_t00" `
        "$BaseOutputDir/${bestMethod}_${ModelKey}_${lang}_t00/"
}

# =============================================================================
# Complete
# =============================================================================
Write-Phase "Together AI Llama 3.3 70B Experiments Complete"

Write-Host "Results saved to: $BaseOutputDir/*_${ModelKey}_*"
Write-Host ""
Write-Host "Experiments completed:"
Get-ChildItem "$BaseOutputDir/*_${ModelKey}_*" -Directory -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  $_" }
