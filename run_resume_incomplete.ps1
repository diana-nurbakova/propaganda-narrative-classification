# =============================================================================
# Resume Incomplete Experiments (PowerShell)
# =============================================================================
# Scans all experiment manifests in results/experiments/ and resumes any that
# have fewer completed runs than expected (n_runs).
#
# Usage:
#   .\run_resume_incomplete.ps1              # Resume all incomplete experiments
#   .\run_resume_incomplete.ps1 -DryRun      # Show what would be resumed without running
#   .\run_resume_incomplete.ps1 -Filter "gpt5nano"  # Only resume matching experiments
# =============================================================================

param(
    [switch]$DryRun,
    [string]$Filter = "",
    [switch]$Help
)

$ErrorActionPreference = "Stop"

if ($Help) {
    Write-Host "Usage: .\run_resume_incomplete.ps1 [-DryRun] [-Filter <pattern>] [-Help]"
    Write-Host ""
    Write-Host "Scans all experiment manifests and resumes incomplete experiments."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -DryRun      Show what would be resumed without actually running"
    Write-Host "  -Filter      Only resume experiments matching this pattern (e.g. 'gpt5nano', 'actor_critic')"
    Write-Host "  -Help        Show this help message"
    exit 0
}

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

$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/core"

# =============================================================================
# Scan for incomplete experiments
# =============================================================================

Write-Host ""
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host "  Scanning for incomplete experiments..." -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host ""

$incomplete = @()

$dirs = Get-ChildItem $BaseOutputDir -Directory -ErrorAction SilentlyContinue
foreach ($dir in $dirs) {
    # Apply filter if specified
    if ($Filter -and $dir.Name -notlike "*$Filter*") {
        continue
    }

    $manifestPath = Join-Path $dir.FullName "experiment_manifest.json"
    if (-not (Test-Path $manifestPath)) {
        continue
    }

    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
    $nRuns = $manifest.n_runs

    # Count runs with success status AND existing result files
    $completedRuns = 0
    foreach ($run in $manifest.runs) {
        if ($run.status -eq "success") {
            $resultFile = $run.output_file
            if ($resultFile -and (Test-Path $resultFile)) {
                $completedRuns++
            }
        }
    }

    if ($completedRuns -lt $nRuns) {
        # Find the config file
        $configPath = $manifest.base_config
        if (-not (Test-Path $configPath)) {
            # Try alternative location
            $configPath = Join-Path $dir.FullName "base_config.yaml"
        }

        $incomplete += @{
            ExperimentId = $manifest.experiment_id
            Dir = $dir.FullName
            NRuns = $nRuns
            CompletedRuns = $completedRuns
            MissingRuns = $nRuns - $completedRuns
            ConfigPath = $configPath
            BaseSeed = if ($manifest.base_seed) { $manifest.base_seed } else { 42 }
        }
    }
}

if ($incomplete.Count -eq 0) {
    Write-Host "All experiments are complete! Nothing to resume." -ForegroundColor Green
    exit 0
}

# Display summary
Write-Host "Found $($incomplete.Count) incomplete experiment(s):" -ForegroundColor Yellow
Write-Host ""
Write-Host ("{0,-45} {1,8} {2,10} {3,8}" -f "Experiment", "Expected", "Completed", "Missing")
Write-Host ("{0,-45} {1,8} {2,10} {3,8}" -f ("-" * 45), ("-" * 8), ("-" * 10), ("-" * 8))

foreach ($exp in $incomplete) {
    $color = if ($exp.CompletedRuns -eq 0) { "Red" } else { "Yellow" }
    Write-Host ("{0,-45} {1,8} {2,10} {3,8}" -f $exp.ExperimentId, $exp.NRuns, $exp.CompletedRuns, $exp.MissingRuns) -ForegroundColor $color
}

Write-Host ""

if ($DryRun) {
    Write-Host "[DRY RUN] Would resume the above experiments. Run without -DryRun to execute." -ForegroundColor Cyan
    exit 0
}

# =============================================================================
# Resume each incomplete experiment
# =============================================================================

$startTime = Get-Date
$succeeded = 0
$failed = 0

foreach ($exp in $incomplete) {
    Write-Host ""
    Write-Host ("=" * 70) -ForegroundColor Green
    Write-Host "  Resuming: $($exp.ExperimentId) ($($exp.MissingRuns) runs remaining)" -ForegroundColor Green
    Write-Host ("=" * 70) -ForegroundColor Green

    if (-not (Test-Path $exp.ConfigPath)) {
        Write-Host "[ERROR] Config not found: $($exp.ConfigPath)" -ForegroundColor Red
        $failed++
        continue
    }

    & $Python src/H3Prompting/run_multi_experiment.py `
        --config $exp.ConfigPath `
        --n-runs $exp.NRuns `
        --experiment-id $exp.ExperimentId `
        --output-dir $exp.Dir `
        --base-seed $exp.BaseSeed `
        --resume `
        --log

    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] $($exp.ExperimentId) completed" -ForegroundColor Green
        $succeeded++
    } else {
        Write-Host "[FAIL] $($exp.ExperimentId) failed with exit code $LASTEXITCODE" -ForegroundColor Red
        $failed++
    }
}

# =============================================================================
# Summary
# =============================================================================

$duration = (Get-Date) - $startTime
Write-Host ""
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host "  Resume Complete" -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host "  Duration: $($duration.ToString('hh\:mm\:ss'))"
Write-Host "  Succeeded: $succeeded" -ForegroundColor Green
Write-Host "  Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host ("=" * 70) -ForegroundColor Cyan
