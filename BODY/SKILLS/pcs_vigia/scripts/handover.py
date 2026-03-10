import os
import json
import glob
import sys
from datetime import datetime
from pathlib import Path

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

def generate_handover():
    mem_root = TerroirLocator.get_mem_root()
    logs_dir = mem_root / "logs_vigia"
    output_file = mem_root / "handover_vigia.json"
    
    echoes = []
    try:
        files = glob.glob(os.path.join(logs_dir, "*.json"))
        files.sort(key=os.path.getmtime, reverse=True)
        
        for file in files[:5]: # Analizar los últimos 5 archivos
            with open(file, 'r', encoding='utf-8') as f:
                echoes.extend(json.load(f))
    except Exception as e:
        print(f"Error leyendo logs: {e}")
        return

    # Esta es una plantilla simplificada. En el uso real, el Vigía usará su propia
    # capacidad cognitiva para llenar estos campos antes de cerrar.
    handover = {
        "timestamp": datetime.now().isoformat(),
        "status": "Vigilia completada",
        "resumen_vigilia": "Vigilia analizada por el sistema de handover.",
        "fricciones_detectadas": [],
        "hitos_logrados": [],
        "future_notions": {
            "thematic_projection": "Continuar desde el último estado de Telegram.",
            "pending_tasks": []
        }
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(handover, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Handover generado en: {output_file}")

if __name__ == "__main__":
    generate_handover()
