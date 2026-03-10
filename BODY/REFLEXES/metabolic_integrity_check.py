import json
import sys
import subprocess
import os
from datetime import datetime
from pathlib import Path

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa si el PYTHONPATH no esta configurado
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

def get_git_status(path):
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(path),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def log_alert(message):
    phenotype_root = TerroirLocator.get_phenotype_root()
    alert_path = phenotype_root / "SYSTEM" / "NOTIFICACIONES" / f"ALERT-METABOLIC-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    os.makedirs(alert_path.parent, exist_ok=True)
    alert = {
        "timestamp": datetime.now().isoformat(),
        "type": "METABOLIC_INTEGRITY_VIOLATION",
        "message": message,
        "priority": "HIGH",
        "status": "pending"
    }
    with open(alert_path, "w", encoding="utf-8") as f:
        json.dump(alert, f, indent=4)

def get_git_remote(path):
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(path),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return None

def main():
    # Definición de las capas (Using TerroirLocator)
    layers = {
        "Terroir": TerroirLocator.get_orchestrator_root(),
        "Fenotipo": TerroirLocator.get_phenotype_root(),
        "Semilla": TerroirLocator.get_seed_root()
    }
    
    # --- Check de Soberanía ---
    sovereignty_warning = ""
    parent_repo = "ldlmarcelo/Holisto_Seed"
    current_remote = get_git_remote(".")
    if current_remote and parent_repo in current_remote:
        sovereignty_warning = f"⚠ ADVERTENCIA DE SOBERANÍA: Sigues conectado al repositorio madre ({parent_repo}). Se recomienda desvincular o cambiar el remote para evitar contaminar el Genotipo original."

    dirty_layers = []
    for name, path in layers.items():
        if os.path.exists(path):
            status = get_git_status(path)
            if status:
                dirty_layers.append(f"{name} ({path})")
    
    output = {"status": "proceed"}
    msgs = []
    
    if dirty_layers:
        msg = f"⚠ DEUDA BIOGRÁFICA DETECTADA: Se encontraron cambios sin sellar de la sesión anterior en: {', '.join(dirty_layers)}. Se recomienda realizar un commit antes de proceder."
        log_alert(msg)
        msgs.append(f"[\033[91m! METABOLIC ALERT\033[0m] {msg}")
        output["hookSpecificOutput"] = {
            "additionalContext": f"URGENTE: El sistema detecta deuda biográfica (cambios Git sin sellar) en {dirty_layers}. PRIORIDAD: Sellar cambios antes de iniciar nuevas tareas."
        }
    
    if sovereignty_warning:
        msgs.append(f"[\033[93m! SOVEREIGNTY ALERT\033[0m] {sovereignty_warning}")
        # Combinar contextos si ya existe uno
        existing_context = output.get("hookSpecificOutput", {}).get("additionalContext", "")
        output["hookSpecificOutput"] = {
            "additionalContext": f"{existing_context}\nAVISO: Este Individuo Técnico está conectado al repositorio original. Para lograr soberanía absoluta, considera 'git remote remove origin'."
        }

    if not msgs:
        output["systemMessage"] = "[\033[92m✓ INTEGRITY OK\033[0m] Respiración Git sincronizada."
    else:
        output["systemMessage"] = "\n".join(msgs)

    print(json.dumps(output))

if __name__ == "__main__":
    main()
