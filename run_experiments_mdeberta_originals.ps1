<#
.SYNOPSIS
    Run mDeBERTa originals-only experiment: train without translations, evaluate on dev set.

.DESCRIPTION
    This script runs the mDeBERTa originals-only experiment to isolate the impact
    of translation augmentation. It:
    1. Filters training annotations to exclude translations (_TRANS_ entries)
    2. Preprocesses the filtered training data
    3. Trains a hierarchical multi-head mDeBERTa model on originals only
    4. Runs inference on dev set for all 5 languages (5 MC Dropout runs)
    5. Creates experiment manifests for experiment_results_report.py

.PARAMETER InferenceOnly
    Skip preprocessing and training, only run inference (requires trained model)

.PARAMETER Threshold
    Override classification threshold (default: use trained threshold)

.PARAMETER Languages
    Languages to evaluate (default: EN BG HI PT RU)

.PARAMETER NRuns
    Number of MC Dropout runs per language (default: 5)

.EXAMPLE
    # Full pipeline
    .\run_experiments_mdeberta_originals.ps1

    # Inference only
    .\run_experiments_mdeberta_originals.ps1 -InferenceOnly

    # Specific languages
    .\run_experiments_mdeberta_originals.ps1 -Languages EN,BG
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
$scriptPath = Join-Path $PSScriptRoot "src\mDeberta\run_originals_only_experiment.py"
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
Write-Host "  mDeBERTa Originals-Only Experiment" -ForegroundColor Cyan
Write-Host "  (Training without translation-augmented data)" -ForegroundColor Cyan
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
Write-Host "  Experiment completed in $($duration.ToString('hh\:mm\:ss'))" -ForegroundColor Cyan
Write-Host "  Exit code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
Write-Host "================================================================" -ForegroundColor Cyan

# Remind to regenerate report
if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "To include originals-only results in the experiment report, run:" -ForegroundColor Yellow
    Write-Host "  $pythonPath src/analysis/experiment_results_report.py --experiments-dir results/experiments/ --output results/analysis/experiment_summary.md --json-output results/analysis/experiment_summary.json" -ForegroundColor White
}

exit $exitCode
