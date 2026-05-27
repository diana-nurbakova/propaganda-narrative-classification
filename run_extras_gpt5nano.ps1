# =============================================================================
# GPT-5 Nano: missing baseline P0, agora P0, agora P0T experiments
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
$NRuns = 3
$BaseOutputDir = "results/experiments"
$ConfigDir = "configs/experiments/generated/emnlp"
$ModelKey = "gpt5nano"

function Run-Exp($config, $id, $out) {
    if (-not (Test-Path $config)) { Write-Host "[ERROR] $config not found" -ForegroundColor Red; return }
    if ((Test-Path $out) -and (Test-Path "$out/experiment_manifest.json")) {
        Write-Host "[SKIP] $id" -ForegroundColor Yellow
        return
    }
    Write-Host "[EXTRAS-GPT] Running: $id ($NRuns runs)" -ForegroundColor Green
    & $Python src/H3Prompting/run_multi_experiment.py --config $config --n-runs $NRuns --experiment-id $id --output-dir $out --log
}

# Generate configs if not present
$missing = @()
$missing += "baseline:bg", "baseline:hi", "baseline:pt", "baseline:ru"
$missing += "agora:en", "agora:bg", "agora:hi", "agora:pt", "agora:ru"
$missing += "agora_p0t:bg", "agora_p0t:hi", "agora_p0t:pt", "agora_p0t:ru"

$methods = @("baseline", "agora", "agora_p0t")
$existing = Get-ChildItem "$ConfigDir/*${ModelKey}*" -ErrorAction SilentlyContinue
& $Python configs/experiments/generate_configs.py `
    --methods @methods `
    --models $ModelKey `
    --temps 0.0 `
    --cost-tracking `
    --vote-saving `
    --output-dir $ConfigDir | Out-Null

Write-Host "`n=== GPT-5 Nano: missing baseline P0 / Agora P0 / Agora P0T ===" -ForegroundColor Cyan

foreach ($entry in $missing) {
    $parts = $entry -split ":"
    $method = $parts[0]
    $lang = $parts[1]
    $id = "${method}_${ModelKey}_${lang}_t00"
    Run-Exp "$ConfigDir/${id}.yaml" $id "$BaseOutputDir/${id}/"
}

Write-Host "`n=== Complete ===" -ForegroundColor Cyan
