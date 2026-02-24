import os
import json
import sys
import shutil
from datetime import datetime

TEMP_FILES = ["knowledge_input.json", "commit_message.txt", "temp_01.png", "knowledge_input.json"]
LOGS_DIR = os.path.join("SYSTEM", "LOGS_MANTENIMIENTO")

def purge_temp():
    """Elimina archivos temporales conocidos en la raíz."""
    purged = []
    for f in TEMP_FILES:
        if os.path.exists(f):
            os.remove(f)
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
