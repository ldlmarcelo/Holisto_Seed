import os
import sys
import subprocess
import time
from pathlib import Path

def get_root_dir():
    # El script está en BODY/UTILS/boot.py
    return Path(__file__).resolve().parent.parent.parent

def get_python_executable():
    root = get_root_dir()
    possible_paths = [
        root / ".venv" / "Scripts" / "python.exe",  # Windows
        root / ".venv" / "bin" / "python",          # Linux/macOS
        root / ".venv" / "bin" / "python3"         # Linux alternativo
    ]
    for path in possible_paths:
        if path.exists():
            return str(path)
    return sys.executable

def check_env():
    root = get_root_dir()
    env_file = root / ".env"
    if not env_file.exists():
        print(f"[!] Error: No se encontró el archivo .env en {root}")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        if "PEGAR_AQUI" in content:
            print("[!] Error: El archivo .env contiene valores de plantilla 'PEGAR_AQUI'.")
            print("[*] Por favor, configure sus credenciales antes de iniciar.")
            return False
    return True

def start_services():
    if not check_env():
        return

    root = get_root_dir()
    python = get_python_executable()
    logs_dir = root / "SYSTEM" / "LOGS_MANTENIMIENTO"
    logs_dir.mkdir(parents=True, exist_ok=True)

    services = [
        {
            "name": "Subconsciente (Daemon)",
            "path": root / "BODY" / "SERVICES" / "daemon.py",
            "log_prefix": "daemon"
        },
        {
            "name": "El Vigía (Telegram)",
            "path": root / "BODY" / "SERVICES" / "vigia" / "main.py",
            "log_prefix": "vigia"
        }
    ]

    print(f"--- Iniciando Terroir (OS: {sys.platform}) ---")
    
    processes = []
    for service in services:
        if not service["path"].exists():
            print(f"[!] No se encontró el script para {service['name']} en {service['path']}")
            continue

        print(f"[*] Despertando {service['name']}...")
        
        stdout_log = open(logs_dir / f"{service['log_prefix']}_stdout.log", "a")
        stderr_log = open(logs_dir / f"{service['log_prefix']}_stderr.log", "a")

        creation_flags = 0
        if sys.platform == "win32":
            # CREATE_NO_WINDOW = 0x08000000
            creation_flags = 0x08000000
        
        # Usamos Popen para que corra en segundo plano de forma independiente
        p = subprocess.Popen(
            [python, str(service["path"])],
            cwd=str(root),
            stdout=stdout_log,
            stderr=stderr_log,
            creationflags=creation_flags,
            start_new_session=True # En Linux equivale a nohup
        )
        processes.append((service["name"], p.pid))
        print(f"    [+] {service['name']} lanzado (PID: {p.pid})")

    print("--- Secuencia de Arranque Completada ---")

def stop_services():
    # Implementación básica para detener por nombre de proceso/script
    # En una versión avanzada podríamos guardar los PIDs en un archivo
    print("[*] Deteniendo servicios del Terroir...")
    if sys.platform == "win32":
        # Comando para Windows usando taskkill buscando scripts de python
        subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/T"], capture_output=True)
    else:
        # Comando para Linux usando pkill
        subprocess.run(["pkill", "-f", "python.*(daemon.py|vigia/main.py)"], capture_output=True)
    print("[+] Servicios detenidos.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python boot.py [start|stop]")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == "start":
        start_services()
    elif command == "stop":
        stop_services()
    else:
        print(f"[!] Comando desconocido: {command}")
