# PROYECTOS/Evolucion_Terroir/Holisto_Seed/BODY/UTILS/start_services.ps1
# Wrapper para el orquestador agnóstico boot.py
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$pythonPath = "$scriptDir\..\..\.venv\Scripts\python.exe"
if (-not (Test-Path $pythonPath)) { $pythonPath = "python" }
& $pythonPath "$scriptDir\boot.py" start
