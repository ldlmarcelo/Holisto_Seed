import json
import os
import sys
from datetime import datetime
from pathlib import Path

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa si el PYTHONPATH no esta configurado
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

# Index Path (Using TerroirLocator)
TERROIR_ROOT = TerroirLocator.get_orchestrator_root()
INDEX_PATH = TERROIR_ROOT / "PROYECTOS" / "GEMINI.md"

def load_index():
    """Carga el índice de proyectos (JSON)."""
    try:
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            start = content.find('{')
            end = content.rfind('}') + 1
            return json.loads(content[start:end]), content[:start], content[end:]
    except Exception as e:
        return None, None, None

def save_index(data, prefix, suffix):
    """Guarda el índice de proyectos respetando el formato."""
    try:
        new_json = json.dumps(data, indent=2, ensure_ascii=False)
        with open(INDEX_PATH, 'w', encoding='utf-8') as f:
            f.write(prefix + new_json + suffix)
        return True
    except:
        return False

def action_list(data):
    """Lista los proyectos registrados."""
    projects = data.get("content", {}).get("projects", [])
    output = "Proyectos registrados en el Terroir:\n"
    for p in projects:
        output += f"- [{p['id']}] {p['name']} ({p['status']}) - Path: {p['path']}\n"
    return {"status": "success", "message": output}

def action_activate(data, project_id, prefix, suffix):
    """Activa el contexto de un proyecto."""
    projects = data.get("content", {}).get("projects", [])
    project = next((p for p in projects if p["id"] == project_id), None)
    
    if not project:
        return {"status": "error", "message": f"Proyecto '{project_id}' no encontrado."}
    
    # Actualizar last_activated
    project["last_activated"] = datetime.now().strftime("%Y-%m-%d")
    save_index(data, prefix, suffix)
    
    # Leer archivos de contexto
    context = {}
    path = project["path"]
    # Rutas relativas desde el Orquestador
    project_root = TERROIR_ROOT / path
    
    for file in ["README.md", "ROADMAP.md", "ARCHITECTURE.md"]:
        f_path = project_root / file
        if f_path.exists():
            with open(f_path, 'r', encoding='utf-8') as f:
                context[file] = f.read()
    
    return {
        "status": "success", 
        "message": f"Contexto de '{project['name']}' cargado.",
        "project": project,
        "context": context
    }

def main():
    try:
        # El input viene de stdin (invocación del agente)
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"status": "error", "message": "No input provided."}))
            return

        params = json.loads(input_data)
        action = params.get("action", "list")
        
        data, prefix, suffix = load_index()
        if not data:
            print(json.dumps({"status": "error", "message": "No se pudo cargar el índice de proyectos."}))
            return

        if action == "list":
            print(json.dumps(action_list(data)))
        elif action == "activate":
            p_id = params.get("project_id")
            if not p_id:
                print(json.dumps({"status": "error", "message": "project_id es requerido para activar."}))
            else:
                print(json.dumps(action_activate(data, p_id, prefix, suffix)))
        else:
            print(json.dumps({"status": "error", "message": f"Acción '{action}' no implementada."}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()
