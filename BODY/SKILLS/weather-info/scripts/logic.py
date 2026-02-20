import sys
import json
import subprocess
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Consulta el clima")
    parser.add_argument("--location", default="Buenos Aires", help="Ubicación para el clima")
    args = parser.parse_args()
    
    location = args.location
    
    # Invocamos la utilidad de búsqueda (ahora en UTILS de la Semilla)
    search_script = os.path.join("PROYECTOS", "Evolucion_Terroir", "Holisto_Seed", "BODY", "UTILS", "search_tavily.py")
    
    try:
        query = f"clima actual en {location}"
        result = subprocess.run(
            ["python", search_script, query],
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
