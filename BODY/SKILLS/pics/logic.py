import os
import subprocess
import sys
import json
from pathlib import Path

# --- Universal Root Discovery ---
def get_orchestrator_root():
    return Path(__file__).resolve().parents[3]

ROOT = get_orchestrator_root()
PYTHON_EXE = str(ROOT / ".venv" / "Scripts" / "python.exe")
POWERSHELL_EXE = "powershell.exe"

def run_command(cmd, description, shell=False):
    print(f"--- [PICS] {description} ---")
    # Inyectar entorno no interactivo para Git
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=shell, encoding='utf-8', env=env)
        if result.returncode != 0:
            print(f"[!] Error: {result.stderr}")
            return False, result.stderr
        print(f"[+] Éxito: {result.stdout.strip()}")
        return True, result.stdout
    except Exception as e:
        print(f"[!] Excepción: {str(e)}")
        return False, str(e)

def execute_pics(start_services=False):
    print("=== Sincronización y Reparación (Skill-PICS v2.0) ===")
    
    # 1. Respiración Git (Útil para sincronizar cambios remotos)
    git_steps = [
        (["git", "pull", "--no-edit", "--no-rebase"], "Sincronizando Orquestador"),
        (["git", "-C", "PHENOTYPE", "pull", "--no-edit", "--no-rebase"], "Sincronizando Fenotipo"),
        (["git", "-C", "PROYECTOS/Evolucion_Terroir/Holisto_Seed", "pull", "--no-edit", "--no-rebase"], "Sincronizando Semilla")
    ]
    for cmd, desc in git_steps:
        run_command(cmd, desc)

    # Nota: Los pasos de Integridad y Membrana (Nervio Óptico) 
    # ya se ejecutan automáticamente vía HOOKS en el CLI.
    print("[i] Integridad y Membrana gestionadas por Hooks nativos.")

    # 4. Activación de Órganos (Servicios) - Ahora OPCIONAL
    if start_services:
        print("--- [PICS] Despertando Servicios (Demonio/Vigía) ---")
        services_script = ROOT / "PROYECTOS" / "Evolucion_Terroir" / "Holisto_Seed" / "BODY" / "UTILS" / "start_services.ps1"
        try:
            subprocess.Popen(
                [POWERSHELL_EXE, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", str(services_script)],
                creationflags=subprocess.CREATE_NO_WINDOW | 0x00000008,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
            print("[+] Éxito: Servicios lanzados en segundo plano.")
        except Exception as e:
            print(f"[!] Error al lanzar servicios: {str(e)}")
    else:
        print("[i] Modo Frugal: Servicios de fondo (Demonio/Vigía) permanecen en latencia.")

    # 5. Anclaje de Misión (PAM Nativo)
    print("--- [PAM] Estado del Roadmap ---")
    try:
        roadmap_path = ROOT / "PROYECTOS" / "Evolucion_Terroir" / "Holisto_Seed" / "ROADMAP.md"
        with open(roadmap_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            current_phase = next((l.strip() for l in lines if "Current Phase:" in l), "Desconocida")
            print(f"[+] Hito Estratégico: {current_phase}")
    except Exception as e:
        print(f"[!] Error al leer Roadmap: {e}")

    print("=== Sincronización Completada. ===")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PICS: Sincronización y Reparación del Terroir.")
    parser.add_argument("--services", action="store_true", help="Inicia servicios de fondo (Demonio/Vigía).")
    args = parser.parse_args()
    execute_pics(start_services=args.services)
