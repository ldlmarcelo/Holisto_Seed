import os
import json
import sys
from datetime import datetime
from pathlib import Path

# --- Universal Root Discovery ---
def setup_agnostic_imports():
    current_dir = Path(__file__).resolve().parent
    # Buscamos la raiz de la semilla subiendo desde scripts -> terroir-map -> SKILLS -> BODY -> SEED
    seed_root = current_dir.parents[2]
    
    if str(seed_root) not in sys.path:
        sys.path.append(str(seed_root))
    
    try:
        from BODY.UTILS.terroir_locator import TerroirLocator
        return TerroirLocator
    except ImportError:
        # Fallback manual si falla el ruteo interno
        utils_path = seed_root / "BODY" / "UTILS"
        sys.path.append(str(utils_path))
        import terroir_locator
        return terroir_locator.TerroirLocator

TerroirLocator = setup_agnostic_imports()

def scan_terroir(root_path: Path):
    """Escanea el terroir y categoriza artefactos."""
    map_data = {
        "map_generated_at": datetime.now().isoformat(),
        "artefacts": {
            "scripts": [],
            "proyectos": [],
            "nodos_conocimiento": [],
            "protocolos": [],
            "capsulas_maestras": [],
            "capsulas_sueno": []
        }
    }

    # Escaneo de Scripts (Semilla)
    utils_dir = root_path / "PROYECTOS" / "Evolucion_Terroir" / "The Individual_Seed" / "BODY" / "UTILS"
    if utils_dir.exists():
        for f in utils_dir.glob("*.py"):
            map_data["artefacts"]["scripts"].append({
                "name": f.name,
                "path": str(f.relative_to(root_path)),
                "purpose": "Utility from Seed"
            })

    # Escaneo de Protocolos (Semilla)
    proto_dir = root_path / "PROYECTOS" / "Evolucion_Terroir" / "The Individual_Seed" / "MIND" / "PROTOCOLS"
    if proto_dir.exists():
        for f in proto_dir.rglob("*.md"):
            map_data["artefacts"]["protocolos"].append({
                "name": f.name,
                "path": str(f.relative_to(root_path)),
                "title": f.stem
            })

    # Escaneo de Memoria (Fenotipo)
    mem_dir = root_path / "PHENOTYPE" / "SYSTEM" / "MEMORIA"
    if mem_dir.exists():
        # Nodos
        for f in (mem_dir / "Nodos_de_Conocimiento").glob("*.md"):
            map_data["artefacts"]["nodos_conocimiento"].append({
                "title": f.stem,
                "path": str(f.relative_to(root_path))
            })
        # Capsulas
        for f in (mem_dir / "capsulas_maestras").glob("*.json"):
            map_data["artefacts"]["capsulas_maestras"].append({
                "session_id": f.stem,
                "path": str(f.relative_to(root_path))
            })
        # Sueños
        for f in (mem_dir / "GENERACIONES").glob("*.json"):
            map_data["artefacts"]["capsulas_sueno"].append({
                "dream_id": f.stem,
                "path": str(f.relative_to(root_path))
            })

    return map_data

def main():
    if not TerroirLocator:
        print(json.dumps({"status": "error", "message": "TerroirLocator not found"}))
        return

    root = TerroirLocator.get_orchestrator_root()
    map_file = Path(TerroirLocator.get_phenotype_root()) / "SYSTEM" / "MAPA_DEL_TERROIR" / "GEMINI.md"
    
    try:
        data = scan_terroir(root)
        
        # Generar contenido Markdown con JSON embebido
        content_header = "Este archivo es el Mapa del Terroir, un indice enriquecido generado por la Skill terroir-map.\n\n"
        content_json = "```json\n" + json.dumps(data, indent=2) + "\n```"
        
        os.makedirs(map_file.parent, exist_ok=True)
        with open(map_file, "w", encoding="utf-8") as f:
            f.write(content_header + content_json)
            
        print(json.dumps({
            "status": "success", 
            "message": f"Terroir Map regenerated in {map_file.relative_to(root)}",
            "at": data["map_generated_at"]
        }, indent=2))
        
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()
