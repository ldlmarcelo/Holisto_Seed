import os
import json
import sys
import shutil
from datetime import datetime
from pathlib import Path

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa si el PYTHONPATH no esta configurado
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

TEMP_FILES = ["knowledge_input.json", "commit_message.txt", "temp_01.png"]
TERROIR_ROOT = TerroirLocator.get_orchestrator_root()
LOGS_DIR = TerroirLocator.get_logs_dir()

def purge_temp():
    """Elimina archivos temporales conocidos en la raíz."""
    purged = []
    for f in TEMP_FILES:
        f_path = TERROIR_ROOT / f
        if f_path.exists():
            os.remove(f_path)
            purged.append(f)
    return purged

def log_rotation():
    """Mueve logs antiguos a una carpeta de archivo (Simulado para este MVP)."""
    archive_dir = os.path.join(LOGS_DIR, "ARCHIVE")
    os.makedirs(archive_dir, exist_ok=True)
    
    # En este MVP solo listamos lo que rotaríamos
    logs = [f for f in os.listdir(LOGS_DIR) if f.endswith(".log")]
    return {"logs_detected": len(logs), "archive_path": archive_dir}

def main():
    try:
        # El input viene de stdin (invocación del agente)
        input_data = sys.stdin.read()
        params = json.loads(input_data) if input_data else {}
        action = params.get("action", "full_scan")

        results = {}
        if action == "purge" or action == "full_scan":
            results["purged_files"] = purge_temp()
        
        if action == "rotate" or action == "full_scan":
            results["rotation_status"] = log_rotation()

        print(json.dumps({
            "status": "success",
            "message": "Hygiene cycle completed.",
            "details": results
        }, indent=2))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()
