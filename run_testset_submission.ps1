# =============================================================================
# Test Set Submission: best language-specific configs (GPT-5 Nano)
# =============================================================================
# Per dev set evaluation, GPT-5 Nano with SC k=3 majority + enriched prompts
# is the strongest configuration. Per-language winners:
#   EN: SC-P1   (sc_3_p1)
#   BG: SC-P1   (sc_3_p1)
#   HI: SC-P2   (sc_3_p2)
#   PT: SC-P2   (sc_3_p2)
#   RU: SC-P2nc (sc_3_p2nc)
#
# Outputs go to results/testset_submissions/{exp}_test/run_{1..N}/
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
    Write-Host "Usage: .\run_testset_submission.ps1 [-NRuns N]"
    Write-Host ""
    Write-Host "Runs the best per-language configuration on the test set."
    Write-Host "  -NRuns    Number of runs per config (default: 3)"
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
    Write-Host "[TESTSET] Running: $expId ($NRuns runs)" -ForegroundColor Green
    & $Python src/H3Prompting/run_multi_experiment.py `
        --config $configFile `
        --n-runs $NRuns `
        --experiment-id $expId `
        --output-dir $outDir `
        --log
}

Write-Host "`n=== Test set submission: GPT-5 Nano ===" -ForegroundColor Cyan
Write-Host "Output dir: $BaseOutputDir"
Write-Host "Runs per config: $NRuns"
Write-Host ""

# Per-language best config
Run-TestExp "sc_3_p1"    "en"
Run-TestExp "sc_3_p1"    "bg"
Run-TestExp "sc_3_p2"    "hi"
Run-TestExp "sc_3_p2"    "pt"
Run-TestExp "sc_3_p2nc"  "ru"

Write-Host "`n=== Test set runs complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: package submission with"
Write-Host "  python scripts/package_submission.py" -ForegroundColor White
