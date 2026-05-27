# =============================================================================
# SC majority with P1 / P2 prompts on GPT-5 Nano
# 1 run per condition (exploratory)
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
    Write-Host "[SC-P1P2-GPT] Running: $id ($NRuns run)" -ForegroundColor Green
    & $Python src/H3Prompting/run_multi_experiment.py --config $config --n-runs $NRuns --experiment-id $id --output-dir $out --log
}

Write-Host "`n=== SC k=3 majority + P1/P2 on GPT-5 Nano ===" -ForegroundColor Yellow

foreach ($method in @("sc_3_p1", "sc_3_p2")) {
    foreach ($lang in $Languages) {
        $id = "${method}_${ModelKey}_${lang}_t00"
        Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
    }
}

Write-Host "`n=== Complete ===" -ForegroundColor Yellow
