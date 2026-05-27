# Run majority/union ablation experiments for 5 and 7 agents
# DeepSeek EN, temperatures 0.0 and 0.7
# 8 experiments x 5 runs each = 40 runs total

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

# --- Majority ablation (5 and 7 agents) ---
Write-Host "`n=== Majority: 5 agents t00 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_5_majority_deepseek_en_t00.yaml" "agora_5_majority_deepseek_en_t00" "$Base/agora_5_majority_deepseek_en_t00/"

Write-Host "`n=== Majority: 5 agents t07 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_5_majority_deepseek_en_t07.yaml" "agora_5_majority_deepseek_en_t07" "$Base/agora_5_majority_deepseek_en_t07/"

Write-Host "`n=== Majority: 7 agents t00 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_7_majority_deepseek_en_t00.yaml" "agora_7_majority_deepseek_en_t00" "$Base/agora_7_majority_deepseek_en_t00/"

Write-Host "`n=== Majority: 7 agents t07 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_7_majority_deepseek_en_t07.yaml" "agora_7_majority_deepseek_en_t07" "$Base/agora_7_majority_deepseek_en_t07/"

# --- Union ablation (5 and 7 agents) ---
Write-Host "`n=== Union: 5 agents t00 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_5_union_deepseek_en_t00.yaml" "agora_5_union_deepseek_en_t00" "$Base/agora_5_union_deepseek_en_t00/"

Write-Host "`n=== Union: 5 agents t07 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_5_union_deepseek_en_t07.yaml" "agora_5_union_deepseek_en_t07" "$Base/agora_5_union_deepseek_en_t07/"

Write-Host "`n=== Union: 7 agents t00 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_7_union_deepseek_en_t00.yaml" "agora_7_union_deepseek_en_t00" "$Base/agora_7_union_deepseek_en_t00/"

Write-Host "`n=== Union: 7 agents t07 ===" -ForegroundColor Blue
Run-Exp "$Cfg/agora_7_union_deepseek_en_t07.yaml" "agora_7_union_deepseek_en_t07" "$Base/agora_7_union_deepseek_en_t07/"

Write-Host "`n=== ALL MAJORITY/UNION ABLATION EXPERIMENTS COMPLETE ===" -ForegroundColor Green
