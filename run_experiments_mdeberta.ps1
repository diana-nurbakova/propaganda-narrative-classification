<#
.SYNOPSIS
    Run mDeBERTa fine-tuned baseline: preprocess, train, and evaluate on all languages.

.DESCRIPTION
    This script orchestrates the full mDeBERTa pipeline:
    1. Preprocess training data from unified annotations
    2. Train hierarchical multi-head mDeBERTa model
    3. Run inference on dev set for all 5 languages (EN, BG, HI, PT, RU)
    4. Create experiment manifests for experiment_results_report.py

.PARAMETER InferenceOnly
    Skip preprocessing and training, only run inference (requires trained model)

.PARAMETER Threshold
    Override classification threshold (default: use trained threshold)

.PARAMETER Languages
    Languages to evaluate (default: EN BG HI PT RU)

.EXAMPLE
    # Full pipeline
    .\run_experiments_mdeberta.ps1

    # Inference only
    .\run_experiments_mdeberta.ps1 -InferenceOnly

    # Custom threshold
    .\run_experiments_mdeberta.ps1 -Threshold 0.3

    # Specific languages
    .\run_experiments_mdeberta.ps1 -Languages EN,BG
#>

param(
    [switch]$InferenceOnly,
    [double]$Threshold = 0,
    [string]$Languages = "",
    [int]$NRuns = 5
)

# Load .env if it exists
$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"').Trim("'")
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
    Write-Host "[OK] Loaded .env file" -ForegroundColor Green
}

# Find Python
$pythonPath = $null
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $pythonPath = $venvPython
    Write-Host "[OK] Using venv Python: $pythonPath" -ForegroundColor Green
} else {
    $pythonPath = "python"
    Write-Host "[WARN] No venv found, using system Python" -ForegroundColor Yellow
}

# Build command args
$scriptPath = Join-Path $PSScriptRoot "src\mDeberta\run_all_languages.py"
$args_list = @($scriptPath)

if ($InferenceOnly) {
    $args_list += "--inference-only"
}

if ($Threshold -gt 0) {
    $args_list += "--threshold"
    $args_list += $Threshold.ToString()
}

if ($Languages -ne "") {
    $args_list += "--languages"
    $Languages.Split(",") | ForEach-Object { $args_list += $_.Trim() }
}

$args_list += "--n-runs"
$args_list += $NRuns.ToString()

# Run
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  mDeBERTa Baseline Pipeline" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Python: $pythonPath"
Write-Host "Script: $scriptPath"
Write-Host "Args: $($args_list[1..($args_list.Length-1)] -join ' ')"
Write-Host ""

$startTime = Get-Date
& $pythonPath $args_list
$exitCode = $LASTEXITCODE
$duration = (Get-Date) - $startTime

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Pipeline completed in $($duration.ToString('hh\:mm\:ss'))" -ForegroundColor Cyan
Write-Host "  Exit code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
Write-Host "================================================================" -ForegroundColor Cyan

# Remind to regenerate report
if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "To include mDeBERTa in the experiment report, run:" -ForegroundColor Yellow
    Write-Host "  $pythonPath src/analysis/experiment_results_report.py --experiments-dir results/experiments/ --output results/analysis/experiment_summary.md --json-output results/analysis/experiment_summary.json" -ForegroundColor White
}

exit $exitCode
