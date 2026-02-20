import sys
import json
import subprocess
import os
import argparse
from pathlib import Path

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa si el PYTHONPATH no esta configurado
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

def main():
    parser = argparse.ArgumentParser(description="Consulta el clima")
    parser.add_argument("--location", default="Buenos Aires", help="Ubicación para el clima")
    args = parser.parse_args()
    
    location = args.location
    
    # Invocamos la utilidad de búsqueda (Using TerroirLocator)
    seed_root = TerroirLocator.get_seed_root()
    search_script = seed_root / "BODY" / "UTILS" / "search_tavily.py"
    
    python_exec = TerroirLocator.get_python_exec()
    
    try:
        query = f"clima actual en {location}"
        result = subprocess.run(
            [python_exec, str(search_script), query],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            weather_data = result.stdout.strip()
            print(json.dumps({
                "status": "ok",
                "location": location,
                "weather": weather_data,
                "message": f"Consciencia climática adquirida para {location}."
            }, ensure_ascii=False))
        else:
            print(json.dumps({"status": "error", "error": "No se pudo obtener información climática."}, ensure_ascii=False))
            
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
