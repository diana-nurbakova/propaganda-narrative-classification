# =============================================================================
# Ensemble Size Ablation: Agora × DeepSeek × EN
# =============================================================================
# Varies the number of agents (1, 3, 5, 7) to measure ensemble size effect.
# 3-agent results (agora_deepseek_en_t0*) should already exist and are skipped.
#
# Usage:
#   .\run_experiments_ensemble_ablation.ps1              # Run all
#   .\run_experiments_ensemble_ablation.ps1 -Generate    # Regenerate configs first
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
    Write-Host ("=" * 77) -ForegroundColor Cyan
    Write-Host "  $msg" -ForegroundColor Cyan
    Write-Host ("=" * 77) -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step($msg) {
    Write-Host "[ENSEMBLE] $msg" -ForegroundColor Green
}

function Show-Usage {
    Write-Host "Usage: .\run_experiments_ensemble_ablation.ps1 [-Generate] [-Help]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Generate    Regenerate config files before running"
    Write-Host "  -Help        Show this help message"
    Write-Host ""
    Write-Host "Experiments:"
    Write-Host "  agora_1  (1-agent)  x DeepSeek x EN x t=0.0, 0.7"
    Write-Host "  agora    (3-agent)  x DeepSeek x EN x t=0.0, 0.7  [already exists]"
    Write-Host "  agora_5  (5-agent)  x DeepSeek x EN x t=0.0, 0.7"
    Write-Host "  agora_7  (7-agent)  x DeepSeek x EN x t=0.0, 0.7"
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
# Main
# =============================================================================

if ($Help) {
    Show-Usage
    exit 0
}

# Generate configs if requested
if ($Generate) {
    Write-Phase "Generating Ensemble Ablation Configs"

    & $Python configs/experiments/generate_configs.py `
        --methods agora_1 agora_5 agora_7 `
        --models deepseek `
        --languages en `
        --temps 0.0 0.7 `
        --cost-tracking `
        --output-dir $ConfigDir
}

# =============================================================================
# Ensemble Size Ablation (temp=0.0)
# =============================================================================
Write-Phase "Ensemble Ablation: DeepSeek EN, temp=0.0"

foreach ($method in @("agora_1", "agora", "agora_5", "agora_7")) {
    Run-Experiment `
        "$ConfigDir/${method}_deepseek_en_t00.yaml" `
        "${method}_deepseek_en_t00" `
        "$BaseOutputDir/${method}_deepseek_en_t00/"
}

# =============================================================================
# Ensemble Size Ablation (temp=0.7)
# =============================================================================
Write-Phase "Ensemble Ablation: DeepSeek EN, temp=0.7"

foreach ($method in @("agora_1", "agora", "agora_5", "agora_7")) {
    Run-Experiment `
        "$ConfigDir/${method}_deepseek_en_t07.yaml" `
        "${method}_deepseek_en_t07" `
        "$BaseOutputDir/${method}_deepseek_en_t07/"
}

# =============================================================================
# Complete
# =============================================================================
Write-Phase "Ensemble Ablation Complete"

Write-Host "Results saved to: $BaseOutputDir/agora*_deepseek_en_*"
Write-Host ""
Write-Host "Experiments:" -ForegroundColor White
Get-ChildItem "$BaseOutputDir/agora*_deepseek_en_*" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $manifest = Join-Path $_.FullName "experiment_manifest.json"
    $status = if (Test-Path $manifest) { "[DONE]" } else { "[MISSING]" }
    Write-Host "  $status $($_.Name)" -ForegroundColor $(if ($status -eq "[DONE]") { "Green" } else { "Red" })
}
Write-Host ""
Write-Host "Next: Run experiment_results_report.py to compare ensemble sizes."
