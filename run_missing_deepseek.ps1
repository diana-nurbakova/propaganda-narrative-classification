# =============================================================================
# DeepSeek V3: missing experiments
# =============================================================================
# Covers the 33 EMNLP DeepSeek experiments that have not been run yet:
#   - baseline_p1, baseline_p2 (deleted earlier due to prefix bug)
#   - sc_3_intersection, sc_3_union (never run for DeepSeek)
#   - agora_majority (BG, HI, RU only -- EN/PT already done)
#   - agora_p1, agora_p2 (never run for DeepSeek)
# =============================================================================

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

if (-not $env:DEEPSEEK_API_KEY) {
    Write-Host "[ERROR] DEEPSEEK_API_KEY not set." -ForegroundColor Red
    exit 1
}

$Python = ".venv\Scripts\python.exe"
$NRuns = 3
$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/emnlp"
$ModelKey = "deepseek"
$AllLanguages = @("en", "bg", "hi", "pt", "ru")

function Run-Exp($config, $id, $out) {
    if (-not (Test-Path $config)) { Write-Host "[ERROR] $config not found" -ForegroundColor Red; return }
    if ((Test-Path $out) -and (Test-Path "$out/experiment_manifest.json") -and (Test-Path "$out/run_1/results.txt")) {
        Write-Host "[SKIP] $id" -ForegroundColor Yellow
        return
    }
    # If a stale (manifest-only, no results) directory exists, remove it
    if ((Test-Path $out) -and (Test-Path "$out/experiment_manifest.json") -and -not (Test-Path "$out/run_1/results.txt")) {
        Write-Host "[CLEAN] removing stale empty experiment: $id" -ForegroundColor DarkYellow
        Remove-Item -Recurse -Force $out
    }
    Write-Host "[MISSING-DS] Running: $id ($NRuns runs)" -ForegroundColor Green
    & $Python src/H3Prompting/run_multi_experiment.py --config $config --n-runs $NRuns --experiment-id $id --output-dir $out --log
}

# Make sure all needed configs exist
$Methods = @(
    "baseline_p1", "baseline_p2",
    "sc_3_intersection", "sc_3_union",
    "agora_majority",
    "agora_p1", "agora_p2"
)
& $Python configs/experiments/generate_configs.py `
    --methods @Methods `
    --models $ModelKey `
    --temps 0.0 `
    --cost-tracking `
    --vote-saving `
    --output-dir $ConfigDir | Out-Null

Write-Host "`n=== DeepSeek: missing P1/P2 + SC variants + Agora ===" -ForegroundColor Magenta

# baseline_p1 / baseline_p2: all 5 langs
foreach ($method in @("baseline_p1", "baseline_p2")) {
    foreach ($lang in $AllLanguages) {
        $id = "${method}_${ModelKey}_${lang}_t00"
        Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
    }
}

# sc_3_intersection / sc_3_union: all 5 langs
foreach ($method in @("sc_3_intersection", "sc_3_union")) {
    foreach ($lang in $AllLanguages) {
        $id = "${method}_${ModelKey}_${lang}_t00"
        Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
    }
}

# agora_majority: only BG, HI, RU (EN, PT already done)
foreach ($lang in @("bg", "hi", "ru")) {
    $id = "agora_majority_${ModelKey}_${lang}_t00"
    Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
}

# agora_p1 / agora_p2: all 5 langs
foreach ($method in @("agora_p1", "agora_p2")) {
    foreach ($lang in $AllLanguages) {
        $id = "${method}_${ModelKey}_${lang}_t00"
        Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
    }
}

Write-Host "`n=== Complete ===" -ForegroundColor Magenta
