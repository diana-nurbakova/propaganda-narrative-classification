# =============================================================================
# Alternative Test Set Submission (after dev offline re-aggregation analysis)
# =============================================================================
# The original test submission used:
#   EN: SC-P1   (sc_3_p1)        -> 1st place
#   BG: SC-P1   (sc_3_p1)        -> good
#   HI: SC-P2   (sc_3_p2)        -> 48% Other on test
#   PT: SC-P2   (sc_3_p2)        -> F1 samples 0.267 (poor)
#   RU: SC-P2nc (sc_3_p2nc)      -> poor
#
# Dev-set offline re-aggregation found better candidates for HI/PT/RU.
# This script runs the underlying multi-agent methods on the test set so we
# can offline re-aggregate them with the winning narrative strategy.
#
# Methods to run:
#   HI: agora_p2  (will offline re-aggregate with union narratives)
#   PT: agora_p2  (will offline re-aggregate with union narratives)
#   RU: agora_p1nc (will offline re-aggregate with majority and union; both)
#   RU: sc_3_p2    (alternative: default majority, no re-agg)
# =============================================================================

param(
    [int]$NRuns = 3,
    [switch]$Help
)

$ErrorActionPreference = "Stop"

# Load .env
$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
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

if (-not $env:OPENAI_API_KEY) {
    Write-Host "[ERROR] OPENAI_API_KEY not set." -ForegroundColor Red
    exit 1
}

$Python = ".venv\Scripts\python.exe"
$BaseOutputDir = "results/testset_submissions"
$ConfigDir = "configs/experiments/generated/testset"

if ($Help) {
    Write-Host "Usage: .\run_testset_submission_alternative.ps1 [-NRuns N]"
    Write-Host ""
    Write-Host "Runs alternative methods on test set so we can offline re-aggregate."
    Write-Host "Methods: agora_p2 (HI, PT), agora_p1nc (RU), sc_3_p2 (RU)"
    exit 0
}

function Run-TestExp($method, $lang) {
    $configFile = "$ConfigDir/${method}_gpt5nano_${lang}_t00.yaml"
    $expId = "${method}_gpt5nano_${lang}_test"
    $outDir = "$BaseOutputDir/${expId}"
    if (-not (Test-Path $configFile)) {
        Write-Host "[ERROR] Config not found: $configFile" -ForegroundColor Red
        return
    }
    if ((Test-Path $outDir) -and (Test-Path "$outDir/experiment_manifest.json") -and (Test-Path "$outDir/run_1/results.txt")) {
        Write-Host "[SKIP] $expId" -ForegroundColor Yellow
        return
    }
    if ((Test-Path $outDir) -and -not (Test-Path "$outDir/run_1/results.txt")) {
        Write-Host "[CLEAN] removing stale empty experiment: $expId" -ForegroundColor DarkYellow
        Remove-Item -Recurse -Force $outDir
    }
    Write-Host "[ALT-TESTSET] Running: $expId ($NRuns runs)" -ForegroundColor Green
    & $Python src/H3Prompting/run_multi_experiment.py `
        --config $configFile `
        --n-runs $NRuns `
        --experiment-id $expId `
        --output-dir $outDir `
        --log
}

Write-Host "`n=== Alternative test set submission: GPT-5 Nano ===" -ForegroundColor Cyan
Write-Host "Output dir: $BaseOutputDir"
Write-Host "Runs per config: $NRuns"
Write-Host ""

# HI: agora_p2 -> offline re-aggregate with union narratives
Run-TestExp "agora_p2"   "hi"

# PT: agora_p2 -> offline re-aggregate with union narratives
Run-TestExp "agora_p2"   "pt"

# RU options
Run-TestExp "agora_p1nc" "ru"   # offline re-aggregate to majority AND union
Run-TestExp "sc_3_p2"    "ru"   # default (majority); no re-agg needed

Write-Host "`n=== Test set runs complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Re-aggregate the test runs offline (narratives only):"
Write-Host "       python scripts/reaggregate_testset.py" -ForegroundColor White
Write-Host ""
Write-Host "  2. Package the new submission:"
Write-Host "       python scripts/package_submission_alternative.py" -ForegroundColor White
