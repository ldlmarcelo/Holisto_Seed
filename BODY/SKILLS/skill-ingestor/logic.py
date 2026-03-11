import sys
import json
import os
from pathlib import Path

# --- Universal Root Discovery ---
# Buscamos la raíz del proyecto para importar el servicio
current_path = Path(__file__).resolve()
terroir_root = None
for parent in current_path.parents:
    if (parent / ".git").exists() or (parent / "requirements.txt").exists():
        terroir_root = parent
        break

if terroir_root:
    sys.path.append(str(terroir_root / "PROYECTOS" / "Evolucion_Terroir" / "Holisto_Seed"))
else:
    # Fallback si no se encuentra la raíz (poco probable en este entorno)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "PROYECTOS", "Evolucion_Terroir", "Holisto_Seed")))

from BODY.SERVICES.skill_ingestor import SkillIngestor

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"status": "error", "message": "No input provided"}))
            return
            
        payload = json.loads(input_data)
        command = payload.get("command")
        args = payload.get("arguments", {})
        
        ingestor = SkillIngestor()
        
        if command == "ingest":
            slug = args.get("slug")
            if not slug:
                print(json.dumps({"status": "error", "message": "Falta el slug de la habilidad"}))
                return
                
            result = ingestor.ingest(slug)
            if result["status"] == "quarantined":
                # Leer el contenido para la auditoría biográfica
                with open(result["path"], "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Generar reporte preliminar
                report = ingestor.audit_report(slug, content)
                result["audit_report"] = report
                
            print(json.dumps(result))
            
        elif command == "assimilate":
            slug = args.get("slug")
            if not slug:
                print(json.dumps({"status": "error", "message": "Falta el slug para asimilar"}))
                return
                
            if ingestor.assimilate(slug):
                print(json.dumps({"status": "success", "message": f"Habilidad '{slug}' asimilada con éxito."}))
            else:
                print(json.dumps({"status": "error", "message": f"No se pudo asimilar '{slug}'. ¿Está en la cuarentena?"}))
        else:
            print(json.dumps({"status": "error", "message": f"Comando desconocido: {command}"}))
            
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()
