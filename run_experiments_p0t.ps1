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
$Python = ".venv\Scripts\python.exe"
$NRuns = 3
$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/emnlp"

function Run-Exp($config, $id, $out) {
    if (-not (Test-Path $config)) { Write-Host "[ERROR] $config not found" -ForegroundColor Red; return }
    if ((Test-Path $out) -and (Test-Path "$out/experiment_manifest.json")) { Write-Host "[SKIP] $id" -ForegroundColor Yellow; return }
    Write-Host "[P0T] Running: $id ($NRuns runs)" -ForegroundColor Green
    & $Python src/H3Prompting/run_multi_experiment.py --config $config --n-runs $NRuns --experiment-id $id --output-dir $out --log
}

Write-Host "`n=== P0T experiments (P0 + ToM, no P1) ===" -ForegroundColor Cyan

foreach ($model in @("deepseek", "together_llama33_70b")) {
    foreach ($method in @("baseline_p0t", "agora_p0t")) {
        foreach ($lang in @("en", "bg", "hi", "pt", "ru")) {
            $id = "${method}_${model}_${lang}_t00"
            Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
        }
    }
}

Write-Host "`n=== P0T experiments complete ===" -ForegroundColor Cyan
