# =============================================================================
# Replicate the original SIGIR-time test submissions on test set
# =============================================================================
# The original repo (commit b8a47d93 "added a bunch of configs for vote based
# classification") used a fundamentally different setup than our EMNLP version:
#
#   - num_narrative_agents = 2  (we used 3 for SC k=3)
#   - num_subnarrative_agents = 1 or 2 (we used 1)
#   - Original simple P0 prompt (NO anti-over-prediction, NO rules, NO ToM)
#   - Mixed aggregation strategies supported
#
# The user reports that those original PT/RU/HI submissions outperformed our
# EMNLP setups on the test set. This script reproduces them.
#
# Methods tested:
#   PT: agora_2_union               (PT narrative_union: 2 narr agents, union)
#   RU: agora_2_union               (RU narrative_union: same as PT)
#   RU: agora_2_full_mixed          (RU full_mixed: narr=union, sub=intersection,
#                                                   2 narr agents, 2 sub agents)
#   HI: agora_2_full_intersection_2sub (HI full_intersection: 2 narr + 2 sub, both intersection)
# Plus other variants for breadth.
# =============================================================================

param(
    [int]$NRuns = 3,
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
$BaseOutputDir = "results/testset_submissions"
$ConfigDir = "configs/experiments/generated/testset"

if ($Help) {
    Write-Host "Usage: .\run_testset_replicate_original.ps1 [-NRuns N]"
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
    Write-Host "[REPLICATE] Running: $expId ($NRuns runs)" -ForegroundColor Green
    & $Python src/H3Prompting/run_multi_experiment.py `
        --config $configFile `
        --n-runs $NRuns `
        --experiment-id $expId `
        --output-dir $outDir `
        --log
}

Write-Host "`n=== Replicating original SIGIR-time test submissions ===" -ForegroundColor Cyan
Write-Host "Methods: agora_2_union, agora_2_intersection, agora_2_full_intersection_2sub,"
Write-Host "         agora_2_full_union_2sub, agora_2_full_mixed"
Write-Host "Languages: HI, PT, RU"
Write-Host "Runs per config: $NRuns"
Write-Host ""

# PT: try original narrative_union (2 narr agents + union)
Run-TestExp "agora_2_union"                   "pt"
Run-TestExp "agora_2_union_p2"                   "pt"

# RU: try narrative_union AND full_mixed (the historical winners)
Run-TestExp "agora_2_union"                   "ru"
Run-TestExp "agora_2_full_mixed"              "ru"
Run-TestExp "agora_2_union_p2"                   "ru"
Run-TestExp "agora_2_full_mixed_p2"              "ru"

# HI: try full_intersection (the historical setup)
Run-TestExp "agora_2_full_intersection_2sub"  "hi"
Run-TestExp "agora_2_full_intersection_2sub_p2"  "hi"

# Also test alternative variants for completeness
#un-TestExp "agora_2_intersection"            "pt"
#un-TestExp "agora_2_intersection"            "ru"
#un-TestExp "agora_2_full_union_2sub"         "hi"
#un-TestExp "agora_2_full_union_2sub"         "pt"
#un-TestExp "agora_2_full_union_2sub"         "ru"
#un-TestExp "agora_2_union"                   "hi"

# EMNLP candidates: sc_3_p2 (3 narr, majority, P2) and agora_p2 (3 narr, intersection, P2)
foreach ($lang in @("hi", "pt", "ru")) {
    Run-TestExp "sc_3_p2"   $lang
    Run-TestExp "agora_p2"  $lang
}

Write-Host "`n=== Replication runs complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Compare prediction patterns to old submissions with:"
Write-Host "  python scripts/compare_with_old_submissions.py" -ForegroundColor White
