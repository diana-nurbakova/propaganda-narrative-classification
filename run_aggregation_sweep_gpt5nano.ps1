# =============================================================================
# Aggregation x prompt sweep for GPT-5 Nano on dev set (HI, PT, RU only)
# =============================================================================
# Tests previously-uncovered aggregation strategies:
#   - SC k=3 with {intersection, union} for P1, P1nc, P2, P2nc
#   - Agora (k=3) with {majority, union} for P1, P1nc, P2, P2nc
#
# Goal: find better-than-current best config for HI/PT/RU before re-submission.
# Current test set issues:
#   HI: sc_3_p2 -> 48% Other rate (over-conservative)
#   PT: sc_3_p2 -> bad despite low Other rate (distribution shift?)
#   RU: sc_3_p2nc -> bad
# =============================================================================

param(
    [int]$NRuns = 3,
    [string[]]$Languages = @("hi", "pt", "ru"),
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
$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/emnlp"
$ModelKey = "gpt5nano"

if ($Help) {
    Write-Host "Usage: .\run_aggregation_sweep_gpt5nano.ps1 [-NRuns N] [-Languages en bg ...]"
    exit 0
}

$Methods = @(
    "sc_3_p1_intersection",   "sc_3_p1_union",
    "sc_3_p2_intersection",   "sc_3_p2_union",
    "sc_3_p1nc_intersection", "sc_3_p1nc_union",
    "sc_3_p2nc_intersection", "sc_3_p2nc_union",
    "agora_p1_majority",      "agora_p1_union",
    "agora_p2_majority",      "agora_p2_union",
    "agora_p1nc_majority",    "agora_p1nc_union",
    "agora_p2nc_majority",    "agora_p2nc_union"
)

function Run-Exp($config, $id, $out) {
    if (-not (Test-Path $config)) { Write-Host "[ERROR] $config not found" -ForegroundColor Red; return }
    if ((Test-Path $out) -and (Test-Path "$out/experiment_manifest.json") -and (Test-Path "$out/run_1/results.txt")) {
        Write-Host "[SKIP] $id" -ForegroundColor Yellow
        return
    }
    if ((Test-Path $out) -and -not (Test-Path "$out/run_1/results.txt")) {
        Write-Host "[CLEAN] removing stale empty experiment: $id" -ForegroundColor DarkYellow
        Remove-Item -Recurse -Force $out
    }
    Write-Host "[AGG-SWEEP] Running: $id ($NRuns runs)" -ForegroundColor Green
    & $Python src/H3Prompting/run_multi_experiment.py `
        --config $config --n-runs $NRuns --experiment-id $id `
        --output-dir $out --log
}

Write-Host "`n=== Aggregation sweep: GPT-5 Nano on $($Languages -join ', ') ===" -ForegroundColor Cyan
Write-Host "  $($Methods.Count) methods x $($Languages.Count) languages = $($Methods.Count * $Languages.Count) experiments"
Write-Host "  $NRuns runs each = $($Methods.Count * $Languages.Count * $NRuns) total runs"
Write-Host ""

foreach ($method in $Methods) {
    foreach ($lang in $Languages) {
        $id = "${method}_${ModelKey}_${lang}_t00"
        Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
    }
}

Write-Host "`n=== Sweep complete ===" -ForegroundColor Cyan
Write-Host "Now run analysis to find new best config per language:"
Write-Host "  python -m src.analysis.enhanced_experiment_report ..." -ForegroundColor White
