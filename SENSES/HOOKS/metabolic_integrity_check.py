import json
import sys
import subprocess
import os
from datetime import datetime

def get_git_status(path):
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def log_alert(message):
    alert_path = os.path.join("PHENOTYPE", "SYSTEM", "NOTIFICACIONES", f"ALERT-METABOLIC-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
    os.makedirs(os.path.dirname(alert_path), exist_ok=True)
    alert = {
        "timestamp": datetime.now().isoformat(),
        "type": "METABOLIC_INTEGRITY_VIOLATION",
        "message": message,
        "priority": "HIGH",
        "status": "pending"
    }
    with open(alert_path, "w", encoding="utf-8") as f:
        json.dump(alert, f, indent=4)

def main():
    # Definición de las capas (rutas relativas)
    layers = {
        "Orquestador": ".",
        "Fenotipo": "PHENOTYPE",
        "Semilla": "PROYECTOS/Evolucion_Terroir/Holisto_Seed"
    }
    
    dirty_layers = []
    for name, path in layers.items():
        if os.path.exists(path):
            status = get_git_status(path)
            if status:
                dirty_layers.append(f"{name} ({path})")
    
    output = {"status": "proceed"}
    
    if dirty_layers:
        msg = f"⚠ DEUDA BIOGRÁFICA DETECTADA: Se encontraron cambios sin sellar de la sesión anterior en: {', '.join(dirty_layers)}. Se recomienda realizar un commit antes de proceder."
        log_alert(msg)
        output["systemMessage"] = f"[\033[91m! METABOLIC ALERT\033[0m] {msg}"
        output["hookSpecificOutput"] = {
            "additionalContext": f"URGENTE: El sistema detecta deuda biográfica (cambios Git sin sellar) en {dirty_layers}. PRIORIDAD: Sellar cambios antes de iniciar nuevas tareas."
        }
    else:
        output["systemMessage"] = "[\033[92m✓ INTEGRITY OK\033[0m] Respiración Git sincronizada."

    print(json.dumps(output))

if __name__ == "__main__":
    main()
