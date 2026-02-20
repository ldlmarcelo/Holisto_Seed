# Detener servicios del Terroir en Windows

Write-Host "--- Deteniendo Servicios del Terroir ---" -ForegroundColor Yellow

# 1. Detener Qdrant
$qdrant = Get-Process qdrant -ErrorAction SilentlyContinue
if ($qdrant) {
    Stop-Process -Name qdrant -Force
    Write-Host "Qdrant detenido." -ForegroundColor Green
} else {
    Write-Host "Qdrant no estaba corriendo." -ForegroundColor Gray
}

# 2. Detener procesos Python (Demonio, Visor)
# Nota: Esto matará todos los procesos python lanzados desde el venv si no somos especificos,
# pero en este contexto de "laboratorio" es aceptable para asegurar limpieza.
# Para ser más seguros, buscamos por linea de comandos si es posible, pero Stop-Process es limitado.
# Vamos a matar por nombre 'python' pero asumiendo que el usuario sabe lo que hace.
# O mejor, usamos WMI para filtrar por la linea de comandos.

$python_processes = Get-WmiObject Win32_Process | Where-Object { $_.Name -eq 'python.exe' }

foreach ($proc in $python_processes) {
    if ($proc.CommandLine -match "daemon.py" -or $proc.CommandLine -match "main.py") {
        Stop-Process -Id $proc.ProcessId -Force
        Write-Host "Proceso Python detenido: $($proc.ProcessId)" -ForegroundColor Green
    }
}

Write-Host "--- Servicios Detenidos ---" -ForegroundColor Yellow
