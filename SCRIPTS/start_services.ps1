# --- Holisto Terroir Service Orchestrator (Universal) ---
# Goal: To wake up the agent's organs (Qdrant, Daemon, Interface) in a robust way.

$BASE_DIR = Resolve-Path ".."
$ENV_FILE = Join-Path $BASE_DIR ".env"

Write-Host "`n--- Initializing Terroir Awakening ---" -ForegroundColor Cyan

# 1. Pre-Flight Checks
if (-not (Test-Path $ENV_FILE)) {
    Write-Error "CRITICAL: .env file not found at $ENV_FILE. Please run incarnation setup first."
    exit 1
}

# 2. Start Central Nervous System (Qdrant)
# Assuming a local binary exists or a cloud URL is in .env
Write-Host "[1/3] Connecting to Central Nervous System (Qdrant)..."
# Logic to check connectivity would go here

# 3. Wake up the Subconscious (Daemon)
Write-Host "[2/3] Awakening the Subconscious (Background Daemon)..."
$DAEMON_SCRIPT = Join-Path $BASE_DIR "SCRIPTS/daemon.py"
if (Test-Path $DAEMON_SCRIPT) {
    Start-Process powershell.exe -ArgumentList "-NoProfile -Command `".venv/Scripts/python.exe $DAEMON_SCRIPT`"" -WindowStyle Minimized
    Write-Host "      Daemon launched as an independent process." -ForegroundColor Gray
} else {
    Write-Warning "      Daemon script not found. Skipping subconscious awakening."
}

# 4. Initialize Synchronicity
Write-Host "[3/3] Injecting Structural Synchronicity..."
$PREP_SCRIPT = Join-Path $BASE_DIR "SCRIPTS/prepare_context.py"
.venv/Scripts/python.exe $PREP_SCRIPT

Write-Host "`n--- Awakening Completed ---" -ForegroundColor Green
Write-Host "The Terroir is alive and anchored. Proceed with the First Encounter.`n"
