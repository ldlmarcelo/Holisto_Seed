# PROYECTOS/Evolucion_Terroir/Holisto_Seed/BODY/UTILS/stop_services.ps1
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$pythonPath = "$scriptDir\..\..\.venv\Scripts\python.exe"
if (-not (Test-Path $pythonPath)) { $pythonPath = "python" }
& $pythonPath "$scriptDir\boot.py" stop
