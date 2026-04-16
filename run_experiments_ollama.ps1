# =============================================================================
# Ollama Model Experiments (PowerShell) - Local or Remote/Authenticated
# =============================================================================
# Run experiments with models via Ollama - either locally or via authenticated endpoint
# Available models: llama3:70b, llama3.3:70b, mistral:7b, qwen3:32b
#
# For authenticated/remote Ollama, set environment variables or use parameters:
#   $env:OLLAMA_BASE_URL = "https://ollama-ui.example.com/ollama"
#   $env:OLLAMA_API_KEY = "your-bearer-token"
# =============================================================================

param(
    [Parameter(Position=0)]
    [string[]]$Models,
    [switch]$All,
    [switch]$Generate,
    [switch]$Help,
    [string]$BaseUrl,
    [string]$ApiKey
)

$ErrorActionPreference = "Stop"

# Model mapping
$ModelKeys = @{
    "llama3"   = "ollama_llama3_70b"
    "llama3.3" = "ollama_llama33_70b"
    "mistral"  = "ollama_mistral_7b"
    "qwen3"    = "ollama_qwen3_32b"
}

$AllModels = @("llama3", "llama3.3", "mistral", "qwen3")
$NRuns = 5
$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/local"

function Write-Phase($msg) {
    Write-Host ""
    Write-Host ("=" * 77) -ForegroundColor Blue
    Write-Host "  $msg" -ForegroundColor Blue
    Write-Host ("=" * 77) -ForegroundColor Blue
    Write-Host ""
}

function Write-Step($msg) {
    Write-Host "[OLLAMA] $msg" -ForegroundColor Green
}

function Write-Warning($msg) {
    Write-Host "[WARN] $msg" -ForegroundColor Yellow
}

function Show-Usage {
    Write-Host "Usage: .\run_experiments_ollama.ps1 [-Models] <model...> [-All] [-Generate] [-BaseUrl URL] [-ApiKey KEY] [-Help]"
    Write-Host ""
    Write-Host "Available models:"
    Write-Host "  llama3    - Llama 3 70B"
    Write-Host "  llama3.3  - Llama 3.3 70B"
    Write-Host "  mistral   - Mistral 7B"
    Write-Host "  qwen3     - Qwen 3 32B"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -BaseUrl URL    Ollama base URL (or set `$env:OLLAMA_BASE_URL)"
    Write-Host "  -ApiKey KEY     Ollama API key (or set `$env:OLLAMA_API_KEY)"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\run_experiments_ollama.ps1 llama3                           # Local"
    Write-Host "  .\run_experiments_ollama.ps1 -All                             # All models locally"
    Write-Host "  .\run_experiments_ollama.ps1 -BaseUrl https://example.com/ollama -ApiKey TOKEN llama3"
    Write-Host ""
    Write-Host "Environment variables:"
    Write-Host "  OLLAMA_BASE_URL    Custom Ollama endpoint URL"
    Write-Host "  OLLAMA_API_KEY     Bearer token for authentication"
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
    python src/H3Prompting/run_multi_experiment.py `
        --config $config `
        --n-runs $NRuns `
        --experiment-id $experimentId `
        --output-dir $outputDir `
        --log
}

function Run-ModelExperiments($modelShort) {
    $modelKey = $ModelKeys[$modelShort]
    if (-not $modelKey) {
        Write-Host "[ERROR] Unknown model: $modelShort" -ForegroundColor Red
        return
    }

    Write-Phase "Running experiments for: $modelShort ($modelKey)"

    # Core methods (EN, temp=0.0)
    Write-Step "Core Methods (EN, temp=0.0)"
    foreach ($method in @("agora", "actor_critic", "baseline")) {
        Run-Experiment `
            "$ConfigDir/${method}_${modelKey}_en_t00.yaml" `
            "${method}_${modelKey}_en_t00" `
            "$BaseOutputDir/${method}_${modelKey}_en_t00/"
    }

    # Temperature comparison (EN, temp=0.7)
    Write-Step "Temperature Comparison (EN, temp=0.7)"
    foreach ($method in @("agora", "actor_critic", "baseline")) {
        Run-Experiment `
            "$ConfigDir/${method}_${modelKey}_en_t07.yaml" `
            "${method}_${modelKey}_en_t07" `
            "$BaseOutputDir/${method}_${modelKey}_en_t07/"
    }

    # Language generalization
    Write-Step "Language Generalization (agora)"
    foreach ($lang in @("bg", "hi", "pt", "ru")) {
        Run-Experiment `
            "$ConfigDir/agora_${modelKey}_${lang}_t00.yaml" `
            "agora_${modelKey}_${lang}_t00" `
            "$BaseOutputDir/agora_${modelKey}_${lang}_t00/"
    }
}

# =============================================================================
# Main
# =============================================================================

if ($Help) {
    Show-Usage
    exit 0
}

if ($All) {
    $Models = $AllModels
}

if (-not $Models -or $Models.Count -eq 0) {
    Write-Host "No models specified." -ForegroundColor Red
    Show-Usage
    exit 1
}

# Resolve auth parameters from env vars if not provided
$OllamaBaseUrl = if ($BaseUrl) { $BaseUrl } else { $env:OLLAMA_BASE_URL }
$OllamaApiKey = if ($ApiKey) { $ApiKey } else { $env:OLLAMA_API_KEY }

# Check Ollama connectivity
Write-Phase "Checking Ollama Status"
if ($OllamaBaseUrl) {
    Write-Step "Using remote Ollama endpoint: $OllamaBaseUrl"
    if ($OllamaApiKey) {
        Write-Step "Authentication: Bearer token configured"
    } else {
        Write-Warning "No API key configured - requests may fail if endpoint requires auth"
    }
} else {
    Write-Step "Using local Ollama (localhost:11434)"
    try {
        $ollamaList = ollama list 2>$null
        Write-Step "Ollama is running"
        Write-Host "Available models:"
        Write-Host $ollamaList
    } catch {
        Write-Warning "Ollama might not be running. Make sure the server is started."
    }
}

# Regenerate configs if requested
if ($Generate) {
    Write-Phase "Regenerating Ollama Configs"

    $generateArgs = @(
        "configs/experiments/generate_configs.py",
        "--methods", "agora", "actor_critic", "baseline",
        "--models", "ollama_llama3_70b", "ollama_llama33_70b", "ollama_mistral_7b", "ollama_qwen3_32b",
        "--temps", "0.0", "0.7",
        "--cost-tracking",
        "--output-dir", $ConfigDir
    )

    if ($OllamaBaseUrl) {
        $generateArgs += "--ollama-base-url"
        $generateArgs += $OllamaBaseUrl
    }
    if ($OllamaApiKey) {
        $generateArgs += "--ollama-api-key"
        $generateArgs += $OllamaApiKey
    }

    & python @generateArgs
}

# Run experiments
Write-Phase "Starting Ollama Experiments"
Write-Host "Models to run: $($Models -join ', ')"

foreach ($model in $Models) {
    Run-ModelExperiments $model
}

Write-Phase "Ollama Experiments Complete"
Write-Host "Results saved to: $BaseOutputDir/*_ollama_*"
