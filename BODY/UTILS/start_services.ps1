# PROYECTOS/Evolucion_Terroir/Holisto_Seed/BODY/UTILS/start_services.ps1
# Script de Orquestación de Servicios del Terroir (v3 - Genotipo Seed)

$ErrorActionPreference = "Stop"

# --- 1. Definicion de Rutas ---
$rootPath = Resolve-Path "."
$venvPath = "$rootPath\.venv"
$pythonPath = "$venvPath\Scripts\python.exe"
$seedPath = "$rootPath\PROYECTOS\Evolucion_Terroir\Holisto_Seed"

$daemonScript = "$seedPath\BODY\SERVICES\daemon.py"
$vigiaScript = "$seedPath\BODY\SERVICES\vigia\main.py"
$logsDir = "$rootPath\SYSTEM\LOGS_MANTENIMIENTO"

# Asegurar directorio de logs
if (-not (Test-Path $logsDir)) { New-Item -ItemType Directory -Path $logsDir -Force | Out-Null }

Write-Host "--- Iniciando Secuencia de Arranque del Terroir (Genotipo Seed) ---" -ForegroundColor Cyan

# --- 2. Iniciar Servicios ---

# Servicio 1: Subconsciente (Daemon)
Write-Host "[1/2] Despertando al Demonio (Subconsciente)..." -ForegroundColor Green
Start-Process -FilePath $pythonPath -ArgumentList "`"$daemonScript`"" -WindowStyle Hidden -WorkingDirectory $rootPath
Write-Host "      Demonio lanzado." -ForegroundColor Cyan

# Servicio 2: Vigia (Telegram Bot)
Write-Host "[2/2] Activando El Vigia (Telegram Bot)..." -ForegroundColor Green
$vigiaOut = "$logsDir\vigia_stdout.log"
$vigiaErr = "$logsDir\vigia_stderr.log"
Start-Process -FilePath $pythonPath -ArgumentList "`"$vigiaScript`"" -WindowStyle Hidden -WorkingDirectory $rootPath -RedirectStandardOutput $vigiaOut -RedirectStandardError $vigiaErr
Write-Host "      El Vigia operativo (Logs: vigia_stdout.log / vigia_stderr.log)." -ForegroundColor Cyan

Write-Host "--- Secuencia de Arranque Completada ---" -ForegroundColor Green
Write-Host "El Terroir esta vivo y anclado en el Genotipo."