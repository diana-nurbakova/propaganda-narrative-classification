# =============================================================================
# GPT-5 Nano Experiments (PowerShell)
# =============================================================================
# Run experiments with GPT-5 Nano via OpenAI API
# Requires: OPENAI_API_KEY in .env or environment
#
# NOTE: GPT-5 Nano requires majority/union aggregation for multi-agent methods.
#       Intersection aggregation produces 80-100% "Other" due to agent disagreement.
#
# Usage:
#   .\run_experiments_gpt5nano.ps1              # Run all experiments
#   .\run_experiments_gpt5nano.ps1 -Generate    # Regenerate configs first
#   .\run_experiments_gpt5nano.ps1 -Clean       # Remove incomplete experiments first
# =============================================================================

param(
    [switch]$Generate,
    [switch]$Clean,
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
    Write-Host "Error: Python not found. Please activate your virtual environment." -ForegroundColor Red
    exit 1
}

Write-Host "Using Python: $Python"

$NRuns = 5
$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/core"
$ModelKey = "gpt5nano"

function Write-Phase($msg) {
    Write-Host ""
    Write-Host ("=" * 77) -ForegroundColor Blue
    Write-Host "  $msg" -ForegroundColor Blue
    Write-Host ("=" * 77) -ForegroundColor Blue
    Write-Host ""
}

function Write-Step($msg) {
    Write-Host "[GPT5NANO] $msg" -ForegroundColor Green
}

function Show-Usage {
    Write-Host "Usage: .\run_experiments_gpt5nano.ps1 [-Generate] [-Clean] [-Help]"
    Write-Host ""
    Write-Host "Runs GPT-5 Nano experiments via OpenAI API."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Generate    Regenerate config files before running"
    Write-Host "  -Clean       Remove incomplete previous experiment results"
    Write-Host "  -Help        Show this help message"
    Write-Host ""
    Write-Host "NOTE: Uses majority aggregation for multi-agent methods."
    Write-Host "      Intersection aggregation causes 80-100% 'Other' with this model."
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

# Clean incomplete experiments if requested
if ($Clean) {
    Write-Phase "Cleaning Incomplete GPT-5 Nano Experiments"

    $dirs = Get-ChildItem "$BaseOutputDir/*_${ModelKey}_*" -Directory -ErrorAction SilentlyContinue
    foreach ($dir in $dirs) {
        $manifest = Join-Path $dir.FullName "experiment_manifest.json"
        if (-not (Test-Path $manifest)) {
            Write-Host "[CLEAN] Removing (no manifest): $($dir.Name)" -ForegroundColor Yellow
            Remove-Item -Recurse -Force $dir.FullName
            continue
        }
        # Check if all runs have results
        $manifestData = Get-Content $manifest | ConvertFrom-Json
        $incomplete = $false
        foreach ($run in $manifestData.runs) {
            $resultFile = Join-Path $dir.FullName "run_$($run.run_id)/results.txt"
            if (-not (Test-Path $resultFile)) {
                $incomplete = $true
                break
            }
        }
        if ($incomplete) {
            Write-Host "[CLEAN] Removing (incomplete runs): $($dir.Name)" -ForegroundColor Yellow
            Remove-Item -Recurse -Force $dir.FullName
        }
    }
}

# Generate configs if requested or missing
$gptConfigs = Get-ChildItem "$ConfigDir/*${ModelKey}*" -ErrorAction SilentlyContinue
if ($Generate -or -not $gptConfigs) {
    Write-Phase "Generating GPT-5 Nano Configs"

    & $Python configs/experiments/generate_configs.py `
        --methods agora_majority agora_union actor_critic baseline `
        --models $ModelKey `
        --temps 0.0 0.7 `
        --cost-tracking `
        --output-dir $ConfigDir
}

# =============================================================================
# Core Method Comparison (EN, temp=0.0)
# NOTE: Using agora_majority instead of agora (intersection) because
#       GPT-5 Nano produces inconsistent labels across agents, causing
#       intersection to empty out -> 80-100% "Other"
# =============================================================================
Write-Phase "GPT-5 Nano: Core Methods (EN, temp=0.0)"

foreach ($method in @("agora_majority", "agora_union", "actor_critic", "baseline")) {
    Run-Experiment `
        "$ConfigDir/${method}_${ModelKey}_en_t00.yaml" `
        "${method}_${ModelKey}_en_t00" `
        "$BaseOutputDir/${method}_${ModelKey}_en_t00/"
}

# =============================================================================
# Temperature Comparison (EN, temp=0.7)
# =============================================================================
Write-Phase "GPT-5 Nano: Temperature Comparison (EN, temp=0.7)"

foreach ($method in @("agora_majority", "agora_union", "actor_critic", "baseline")) {
    Run-Experiment `
        "$ConfigDir/${method}_${ModelKey}_en_t07.yaml" `
        "${method}_${ModelKey}_en_t07" `
        "$BaseOutputDir/${method}_${ModelKey}_en_t07/"
}

# =============================================================================
# Language Generalization (agora_majority across languages)
# =============================================================================
Write-Phase "GPT-5 Nano: Language Generalization"

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
Write-Phase "GPT-5 Nano Experiments Complete"

Write-Host "Results saved to: $BaseOutputDir/*_${ModelKey}_*"
Write-Host ""
Write-Host "Experiments completed:"
Get-ChildItem "$BaseOutputDir/*_${ModelKey}_*" -Directory -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  $_" }
