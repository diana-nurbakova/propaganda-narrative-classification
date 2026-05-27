# =============================================================================
# GPT-5 Nano: P1nc / P2nc -- no-conservative variants of P1 / P2
# Tests whether annotation rules + BERTopic keywords (+ ToM) help GPT-5 Nano
# when NOT paired with the "be conservative" instruction.
# 1 run per condition (exploratory).
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

if (-not $env:OPENAI_API_KEY) {
    Write-Host "[ERROR] OPENAI_API_KEY not set." -ForegroundColor Red
    exit 1
}

$Python = ".venv\Scripts\python.exe"
$NRuns = 1
$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/emnlp"
$ModelKey = "gpt5nano"
$Languages = @("en", "bg", "hi", "pt", "ru")

function Run-Exp($config, $id, $out) {
    if (-not (Test-Path $config)) { Write-Host "[ERROR] $config not found" -ForegroundColor Red; return }
    if ((Test-Path $out) -and (Test-Path "$out/experiment_manifest.json")) {
        Write-Host "[SKIP] $id" -ForegroundColor Yellow
        return
    }
    Write-Host "[P1nc/P2nc-GPT] Running: $id ($NRuns run)" -ForegroundColor Green
    & $Python src/H3Prompting/run_multi_experiment.py --config $config --n-runs $NRuns --experiment-id $id --output-dir $out --log
}

Write-Host "`n=== GPT-5 Nano: P1nc / P2nc (no-conservative variants) ===" -ForegroundColor Yellow

# Baseline (single-agent) with no-conservative P1/P2
foreach ($method in @("baseline_p1nc", "baseline_p2nc")) {
    foreach ($lang in $Languages) {
        $id = "${method}_${ModelKey}_${lang}_t00"
        Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
    }
}

# SC k=3 with no-conservative P1/P2
foreach ($method in @("sc_3_p1nc", "sc_3_p2nc")) {
    foreach ($lang in $Languages) {
        $id = "${method}_${ModelKey}_${lang}_t00"
        Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
    }
}

# Agora (3-agent intersection) with no-conservative P1/P2
foreach ($method in @("agora_p1nc", "agora_p2nc")) {
    foreach ($lang in $Languages) {
        $id = "${method}_${ModelKey}_${lang}_t00"
        Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
    }
}

Write-Host "`n=== Complete ===" -ForegroundColor Yellow
Write-Host "Compare with existing GPT-5 Nano results:" -ForegroundColor Cyan
Write-Host "  P1 (with conservative block)  vs  P1nc (without)"
Write-Host "  P2 (with conservative block)  vs  P2nc (without)"
