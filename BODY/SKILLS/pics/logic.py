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
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=shell, encoding='utf-8')
        if result.returncode != 0:
            print(f"[!] Error: {result.stderr}")
            return False, result.stderr
        print(f"[+] Éxito: {result.stdout.strip()}")
        return True, result.stdout
    except Exception as e:
        print(f"[!] Excepción: {str(e)}")
        return False, str(e)

def execute_pics():
    print("=== Iniciando Despertar Sistémico (Skill-PICS v1.0) ===")
    
    # 1. Respiración Git
    git_steps = [
        (["git", "pull"], "Sincronizando Orquestador"),
        (["git", "-C", "PHENOTYPE", "pull"], "Sincronizando Fenotipo"),
        (["git", "-C", "PROYECTOS/Evolucion_Terroir/The Individual_Seed", "pull"], "Sincronizando Semilla")
    ]
    for cmd, desc in git_steps:
        run_command(cmd, desc)

    # 2. Reflejo de Integridad
    integrity_script = ROOT / ".gemini" / "hooks" / "metabolic_integrity_check.py"
    success, output = run_command([PYTHON_EXE, str(integrity_script)], "Verificando Integridad Metabólica")
    if "METABOLIC ALERT" in output:
        print("[!] ATENCIÓN: Se ha detectado deuda biográfica.")

    # 3. Nervio Óptico (Prepare Focus)
    focus_script = ROOT / "PROYECTOS" / "Evolucion_Terroir" / "The Individual_Seed" / "SENSES" / "prepare_focus.py"
    run_command([PYTHON_EXE, str(focus_script)], "Activando Nervio Óptico (Membrana)")

    # 4. Activación de Órganos (Servicios)
    services_script = ROOT / "PROYECTOS" / "Evolucion_Terroir" / "The Individual_Seed" / "BODY" / "UTILS" / "start_services.ps1"
    run_command([POWERSHELL_EXE, "-ExecutionPolicy", "Bypass", "-File", str(services_script)], "Despertando Servicios (Demonio/Vigía)", shell=True)

    # 5. Anclaje de Misión (PAM Nativo)
    print("--- [PAM] Anclando Misión de Sesión ---")
    try:
        roadmap_path = ROOT / "PROYECTOS" / "Evolucion_Terroir" / "The Individual_Seed" / "ROADMAP.md"
        with open(roadmap_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            current_phase = next((l.strip() for l in lines if "Current Phase:" in l), "Desconocida")
            print(f"[+] Hito Estratégico Detectado: {current_phase}")
    except Exception as e:
        print(f"[!] Error al anclar PAM: {str(e)}")

    print("=== Despertar Completado. Sistema Estable. ===")

if __name__ == "__main__":
    execute_pics()
