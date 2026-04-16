# Run remaining DeepSeek EN experiments
# - 3 aggregation strategy experiments (majority_t07, union_t00, union_t07)
# - 3 ablation t07 experiments (agora_1, agora_5, agora_7)

$ErrorActionPreference = "Stop"

# Load .env
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

$Python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
Write-Host "Using Python: $Python"

$NRuns = 5
$Base = "results/experiments"
$Cfg = "configs/experiments/generated/core"

function Run-Exp($config, $id, $dir) {
    if (-not (Test-Path $config)) {
        Write-Host "[ERROR] Config not found: $config" -ForegroundColor Red
        return
    }
    if ((Test-Path $dir) -and (Test-Path "$dir/experiment_manifest.json")) {
        Write-Host "[SKIP] $id already exists" -ForegroundColor Yellow
        return
    }
    Write-Host "[RUN] $id" -ForegroundColor Green
    & $Python src/H3Prompting/run_multi_experiment.py `
        --config $config --n-runs $NRuns --experiment-id $id --output-dir $dir --log
}

function Resume-Exp($config, $id, $dir) {
    Write-Host "[RESUME] $id" -ForegroundColor Cyan
    & $Python src/H3Prompting/run_multi_experiment.py `
        --config $config --n-runs $NRuns --experiment-id $id --output-dir "$dir/" --resume --log
}

# --- Aggregation strategy experiments ---
Write-Host "`n=== Aggregation: majority t07 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_majority_deepseek_en_t07.yaml" "agora_majority_deepseek_en_t07" "$Base/agora_majority_deepseek_en_t07/"

Write-Host "`n=== Aggregation: union t00 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_union_deepseek_en_t00.yaml" "agora_union_deepseek_en_t00" "$Base/agora_union_deepseek_en_t00/"

Write-Host "`n=== Aggregation: union t07 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_union_deepseek_en_t07.yaml" "agora_union_deepseek_en_t07" "$Base/agora_union_deepseek_en_t07/"

# --- Ablation t07 experiments ---
Write-Host "`n=== Ablation: agora_1 t07 (resume 1/5) ===" -ForegroundColor Blue
Resume-Exp "$Cfg/agora_1_deepseek_en_t07.yaml" "agora_1_deepseek_en_t07" "$Base/agora_1_deepseek_en_t07"

Write-Host "`n=== Ablation: agora_5 t07 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_5_deepseek_en_t07.yaml" "agora_5_deepseek_en_t07" "$Base/agora_5_deepseek_en_t07/"

Write-Host "`n=== Ablation: agora_7 t07 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_7_deepseek_en_t07.yaml" "agora_7_deepseek_en_t07" "$Base/agora_7_deepseek_en_t07/"

Write-Host "`n=== ALL EXPERIMENTS COMPLETE ===" -ForegroundColor Green
