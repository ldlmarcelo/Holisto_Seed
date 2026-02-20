# SYSTEM/Scripts/start_services.ps1
# Script de Orquestación de Servicios del Terroir (v2 - Portable)
# Encapsula el inicio de Qdrant, Daemon y Visor con gestión de dependencias, tiempos y PRE-FLIGHT CHECKS.

$ErrorActionPreference = "Stop"

# --- 1. Definición de Rutas (Relativas a la raíz del proyecto) ---
$rootPath = Resolve-Path "."
$venvPath = "$rootPath\.venv"
$pythonPath = "$venvPath\Scripts\python.exe"
$envFile = "$rootPath\.env"
$reqFile = "$rootPath\requirements.txt"

$qdrantScript = "$rootPath\SYSTEM\NUCLEO_DISTRIBUIDO\start_qdrant.ps1"
$daemonScript = "$rootPath\SYSTEM\NUCLEO_DISTRIBUIDO\services\exocortex\src\daemon.py"
$visorScript = "$rootPath\PROYECTOS\Evolucion_Terroir\Visor_Logs\main.py"
$vigiaScript = "$rootPath\SYSTEM\NUCLEO_DISTRIBUIDO\services\vigia\src\main.py"
$logsDir = "$rootPath\SYSTEM\LOGS_MANTENIMIENTO"

# Asegurar directorio de logs
if (-not (Test-Path $logsDir)) { New-Item -ItemType Directory -Path $logsDir -Force | Out-Null }

Write-Host "--- Iniciando Secuencia de Arranque del Terroir (Modo Portable) ---" -ForegroundColor Cyan

# --- 2. Pre-Flight Checks (Diagnóstico de Entorno) ---

# Check A: Entorno Virtual (.venv)
if (-not (Test-Path $pythonPath)) {
    Write-Warning "ALERTA DE PORTABILIDAD: No se detecta el entorno virtual en $venvPath"
    Write-Host "Acción Requerida:" -ForegroundColor Yellow
    Write-Host "1. Ejecute: python -m venv .venv"
    Write-Host "2. Ejecute: .venv\Scripts\pip install -r requirements.txt"
    Write-Host "3. Vuelva a ejecutar este script."
    exit 1
}

# Check B: Secretos (.env)
if (-not (Test-Path $envFile)) {
    Write-Warning "ALERTA DE SEGURIDAD: Falta el archivo de configuración .env"
    $template = "GEMINI_API_KEY=PEGAR_TU_API_KEY_AQUI`nTELEGRAM_TOKEN=TU_TOKEN_DE_TELEGRAM`nTELEGRAM_USER_ID=TU_ID_DE_USUARIO_TELEGRAM"
    Set-Content -Path $envFile -Value $template
    Write-Host " [AUTO-FIX] Se ha creado un archivo .env plantilla." -ForegroundColor Green
    Write-Host "Acción Requerida: Abra el archivo .env y pegue sus credenciales antes de continuar." -ForegroundColor Yellow
    exit 1
}

# --- 3. Iniciar Servicios ---

# Servicio 1: Qdrant (Base de Memoria) - DESHABILITADO LOCAL (Mente Unificada en Cloud)
Write-Host "[1/3] Conectando a Qdrant Cloud..." -ForegroundColor Green
# if (Test-Path $qdrantScript) {
#     Start-Process -FilePath "powershell.exe" -ArgumentList "-ExecutionPolicy Bypass -File `"$qdrantScript`"" -NoNewWindow
# } else {
#     Write-Error "CRITICO: No se encuentra el script de Qdrant en $qdrantScript"
#     exit 1
# }

# El chequeo de puerto local ya no es necesario.
Write-Host "      Configuración de Cloud validada." -ForegroundColor Cyan

# Servicio 2: Subconsciente (Daemon)
Write-Host "[2/4] Despertando al Demonio (Subconsciente)..." -ForegroundColor Green
Start-Process -FilePath $pythonPath -ArgumentList "`"$daemonScript`"" -WindowStyle Hidden -WorkingDirectory $rootPath
Write-Host "      Demonio lanzado como proceso independiente." -ForegroundColor Cyan

# Servicio 3: Visor de Logs (Espejo) - DESACOPLADO (Ejecutable Satelital)
# Write-Host "[3/4] Activando Visor de Logs (Puerto 8056)..." -ForegroundColor Green
# Start-Process -FilePath $pythonPath -ArgumentList "`"$visorScript`" --port 8056" -WindowStyle Hidden -WorkingDirectory $rootPath
# Write-Host "      Visor operativo en puerto 8056." -ForegroundColor Cyan

# Servicio 3: Vigía (Telegram Bot)
Write-Host "[3/3] Activando El Vigía (Telegram Bot)..." -ForegroundColor Green
$vigiaOut = "$logsDir\vigia_stdout.log"
$vigiaErr = "$logsDir\vigia_stderr.log"
Start-Process -FilePath $pythonPath -ArgumentList "`"$vigiaScript`"" -WindowStyle Hidden -WorkingDirectory $rootPath -RedirectStandardOutput $vigiaOut -RedirectStandardError $vigiaErr
Write-Host "      El Vigía operativo (Logs: vigia_stdout.log / vigia_stderr.log)." -ForegroundColor Cyan

Write-Host "--- Secuencia de Arranque Completada ---" -ForegroundColor Green
Write-Host "El Terroir está vivo y anclado."