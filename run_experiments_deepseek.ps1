# =============================================================================
# DeepSeek EN Experiments (PowerShell)
# =============================================================================
# Run DeepSeek experiments for voting failure analysis:
#   - 3 aggregation strategies (intersection, majority, union) x 2 temperatures
#   - Agent count ablation (1, 3, 5, 7 agents)
#   - All with vote saving enabled where applicable
#
# Usage:
#   .\run_experiments_deepseek.ps1              # Run all experiments
#   .\run_experiments_deepseek.ps1 -Generate    # Regenerate configs first
#   .\run_experiments_deepseek.ps1 -AblationOnly # Only run ablation experiments
# =============================================================================

param(
    [switch]$Generate,
    [switch]$AblationOnly,
    [switch]$Help
)

$ErrorActionPreference = "Stop"

# Load .env file if it exists
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

# Detect Python
$Python = $null
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $Python = $venvPython
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $Python = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $Python = "python3"
} else {
    Write-Host "Error: Python not found. Please activate your virtual environment." -ForegroundColor Red
    exit 1
}

Write-Host "Using Python: $Python"

$NRuns = 5
$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/core"

function Write-Phase($msg) {
    Write-Host ""
    Write-Host ("=" * 77) -ForegroundColor Cyan
    Write-Host "  $msg" -ForegroundColor Cyan
    Write-Host ("=" * 77) -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step($msg) {
    Write-Host "[DEEPSEEK] $msg" -ForegroundColor Green
}

function Show-Usage {
    Write-Host "Usage: .\run_experiments_deepseek.ps1 [-Generate] [-AblationOnly] [-Help]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Generate      Regenerate config files before running"
    Write-Host "  -AblationOnly  Only run agent count ablation experiments"
    Write-Host "  -Help          Show this help message"
}

function Run-Experiment($config, $experimentId, $outputDir) {
    if (-not (Test-Path $config)) {
        Write-Host "[ERROR] Config not found: $config" -ForegroundColor Red
        return
    }

    if ((Test-Path $outputDir) -and (Test-Path "$outputDir/experiment_manifest.json")) {
        Write-Host "[SKIP] $experimentId already exists" -ForegroundColor Yellow
        return
    }

    Write-Step "Running: $experimentId"
    & $Python src/H3Prompting/run_multi_experiment.py `
        --config $config `
        --n-runs $NRuns `
        --experiment-id $experimentId `
        --output-dir $outputDir `
        --log
}

# =============================================================================
# Main
# =============================================================================

if ($Help) {
    Show-Usage
    exit 0
}

# Generate configs if requested
if ($Generate) {
    Write-Phase "Generating DeepSeek Configs"

    & $Python configs/experiments/generate_configs.py `
        --methods agora agora_majority agora_union agora_1 agora_5 agora_7 `
        --models deepseek `
        --languages en `
        --temps 0.0 0.7 `
        --cost-tracking `
        --vote-saving `
        --output-dir $ConfigDir
}

if (-not $AblationOnly) {
    # =============================================================================
    # Aggregation Strategy Comparison (EN, temp=0.0)
    # =============================================================================
    Write-Phase "DeepSeek: Aggregation Strategies (EN, temp=0.0)"

    foreach ($method in @("agora_majority", "agora_union")) {
        Run-Experiment `
            "$ConfigDir/${method}_deepseek_en_t00.yaml" `
            "${method}_deepseek_en_t00" `
            "$BaseOutputDir/${method}_deepseek_en_t00/"
    }

    # =============================================================================
    # Aggregation Strategy Comparison (EN, temp=0.7)
    # =============================================================================
    Write-Phase "DeepSeek: Aggregation Strategies (EN, temp=0.7)"

    foreach ($method in @("agora_majority", "agora_union")) {
        Run-Experiment `
            "$ConfigDir/${method}_deepseek_en_t07.yaml" `
            "${method}_deepseek_en_t07" `
            "$BaseOutputDir/${method}_deepseek_en_t07/"
    }
}

# =============================================================================
# Agent Count Ablation (EN, temp=0.0) - resume incomplete agora_7
# =============================================================================
Write-Phase "DeepSeek: Agent Count Ablation (EN, temp=0.0)"

# agora_1 and agora_5 should already exist and will be skipped
foreach ($method in @("agora_1", "agora_5")) {
    Run-Experiment `
        "$ConfigDir/${method}_deepseek_en_t00.yaml" `
        "${method}_deepseek_en_t00" `
        "$BaseOutputDir/${method}_deepseek_en_t00/"
}

# agora_7: resume incomplete experiment (has manifest with 1/5 runs)
$agora7Dir = "$BaseOutputDir/agora_7_deepseek_en_t00"
$agora7Manifest = "$agora7Dir/experiment_manifest.json"
$agora7Config = "$ConfigDir/agora_7_deepseek_en_t00.yaml"
if ((Test-Path $agora7Manifest)) {
    $manifest = Get-Content $agora7Manifest -Raw | ConvertFrom-Json
    $completedRuns = ($manifest.runs | Where-Object { $_.status -eq "success" }).Count
    if ($completedRuns -lt $manifest.n_runs) {
        Write-Step "Resuming agora_7_deepseek_en_t00 ($completedRuns/$($manifest.n_runs) runs complete)"
        & $Python src/H3Prompting/run_multi_experiment.py `
            --config $agora7Config `
            --n-runs $NRuns `
            --experiment-id "agora_7_deepseek_en_t00" `
            --output-dir "$agora7Dir/" `
            --resume `
            --log
    } else {
        Write-Host "[SKIP] agora_7_deepseek_en_t00 already complete" -ForegroundColor Yellow
    }
} else {
    Run-Experiment `
        $agora7Config `
        "agora_7_deepseek_en_t00" `
        "$agora7Dir/"
}

# =============================================================================
# Complete
# =============================================================================
Write-Phase "DeepSeek EN Experiments Complete"

Write-Host "Results saved to: $BaseOutputDir/*_deepseek_en_*"
Write-Host ""
Write-Host "Experiments:"
Get-ChildItem "$BaseOutputDir/*_deepseek_en_*" -Directory -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  $_" }
