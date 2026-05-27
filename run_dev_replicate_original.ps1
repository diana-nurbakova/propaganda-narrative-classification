# =============================================================================
# Dev set sweep: k=2 agent variants (original SIGIR setup) x all prompts
# =============================================================================
# Tests the original "Agora 2 narrative agents" setup with all our prompt
# levels (P0, P0', P1, P1nc, P2, P2nc) on HI/PT/RU dev set, to find which
# combination best matches the test set behavior.
#
# Methods tested (19 methods x 3 langs = 57 experiments):
#   2-narr + 1-sub agents:
#     agora_2_union          (P0)    agora_2_intersection          (P0)
#     agora_2_union_p0prime          agora_2_intersection_p0prime
#     agora_2_union_p1               agora_2_intersection_p1
#     agora_2_union_p1nc
#     agora_2_union_p2               agora_2_intersection_p2
#     agora_2_union_p2nc
#   2-narr + 2-sub agents:
#     agora_2_full_intersection_2sub          (P0)
#     agora_2_full_intersection_2sub_p0prime
#     agora_2_full_intersection_2sub_p1
#     agora_2_full_intersection_2sub_p2
#     agora_2_full_union_2sub                 (P0)
#     agora_2_full_union_2sub_p0prime
#     agora_2_full_union_2sub_p1
#     agora_2_full_union_2sub_p2               
#     agora_2_full_mixed                      (P0)  (narr=union, sub=intersection)
#     agora_2_full_mixed_p0prime
#     agora_2_full_mixed_p1
#     agora_2_full_mixed_p2
# =============================================================================

param(
    [int]$NRuns = 3,
    [string[]]$Languages = @("hi", "pt", "ru"),
    [switch]$Help
)

$ErrorActionPreference = "Stop"

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
#$ModelKey = "gpt5nano"
$ModelKey = "deepseek"

if ($Help) {
    Write-Host "Usage: .\run_dev_replicate_original.ps1 [-NRuns N] [-Languages hi pt ru]"
    exit 0
}

$Methods = @(
    # 2-narr + 1-sub agents
    "agora_2_union", "agora_2_intersection",
    "agora_2_union_p0prime", "agora_2_intersection_p0prime",
    "agora_2_union_p1",      "agora_2_intersection_p1",
    "agora_2_union_p1nc",
    "agora_2_union_p2",      "agora_2_intersection_p2",
    "agora_2_union_p2nc",
    # 2-narr + 2-sub agents
    "agora_2_full_intersection_2sub",
    "agora_2_full_intersection_2sub_p0prime",
    "agora_2_full_intersection_2sub_p1",
    "agora_2_full_intersection_2sub_p2",
    "agora_2_full_union_2sub",
    "agora_2_full_mixed",
    "agora_2_full_mixed_p0prime",
    "agora_2_full_mixed_p1",
    "agora_2_full_mixed_p2",
    "agora_2_full_union_2sub_p0prime",
    "agora_2_full_union_2sub_p1",
    "agora_2_full_union_2sub_p2"
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
    Write-Host "[REPL-DEV] Running: $id ($NRuns runs)" -ForegroundColor Green
    & $Python src/H3Prompting/run_multi_experiment.py `
        --config $config --n-runs $NRuns --experiment-id $id `
        --output-dir $out --log
}

#Write-Host "`n=== Original-style sweep on dev: GPT-5 Nano on $($Languages -join ', ') ===" -ForegroundColor Cyan
Write-Host "`n=== Original-style sweep on dev: Deepseek on $($Languages -join ', ') ===" -ForegroundColor Cyan
Write-Host "  $($Methods.Count) methods x $($Languages.Count) langs = $($Methods.Count * $Languages.Count) experiments"
Write-Host "  $NRuns runs each = $($Methods.Count * $Languages.Count * $NRuns) total runs"
Write-Host ""

foreach ($method in $Methods) {
    foreach ($lang in $Languages) {
        $id = "${method}_${ModelKey}_${lang}_t00"
        Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
    }
}

Write-Host "`n=== Sweep complete ===" -ForegroundColor Cyan
Write-Host "Refresh analysis with:"
Write-Host "  python -m src.analysis.enhanced_experiment_report ..." -ForegroundColor White
