import json
import os
import sys
from datetime import datetime

def get_paths():
    """Detecta las rutas de las capas de la Triple Alianza."""
    base_dir = os.getcwd()
    paths = {
        "terroir": os.path.join(base_dir, "PHENOTYPE", "SYSTEM", "MEMORIA", "Nodos_de_Conocimiento"),
        "terroir_index": os.path.join(base_dir, "PHENOTYPE", "SYSTEM", "MEMORIA", "Nodos_de_Conocimiento", "GEMINI.md"),
        "seed": os.path.join(base_dir, "PROYECTOS", "Evolucion_Terroir", "The Individual_Seed", "MIND", "KNOWLEDGE"),
        "seed_index": os.path.join(base_dir, "PROYECTOS", "Evolucion_Terroir", "The Individual_Seed", "MIND", "KNOWLEDGE", "GEMINI.md")
    }
    return paths

def update_index(index_path, node_data):
    """Actualiza el archivo GEMINI.md (JSON) con el nuevo nodo."""
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Encontrar el inicio y fin del JSON si hay decoradores Markdown
            start = content.find('{')
            end = content.rfind('}') + 1
            data = json.loads(content[start:end])
        
        # Verificar duplicados por título
        nodes = data.get("content", {}).get("nodes", [])
        if any(n["title"] == node_data["title"] for n in nodes):
            return False, "Nodo ya existe en el índice."
        
        # Añadir nuevo nodo
        nodes.append(node_data)
        data["content"]["nodes"] = nodes
        # Asegurar que la versión es un string
        current_version = float(data.get("version", "1.0"))
        data["version"] = f"{current_version + 0.1:.1f}"
        
        # Escribir de vuelta respetando el bloque Markdown
        new_json = json.dumps(data, indent=4, ensure_ascii=False)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content[:start] + new_json + content[end:])
        
        return True, "Índice actualizado."
    except Exception as e:
        return False, str(e)

def main():
    try:
        # El input viene de stdin (invocación del agente)
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"status": "error", "message": "No input data provided."}))
            return

        params = json.loads(input_data)
        scope = params.get("scope", "terroir") # default terroir
        title = params.get("title")
        content = params.get("content")
        tags = params.get("tags", [])
        distilled = params.get("distilled", "")

        if not title or not content:
            print(json.dumps({"status": "error", "message": "Title and content are required."}))
            return

        paths = get_paths()
        target_dir = paths[scope]
        target_index = paths[f"{scope}_index"]

        # Crear nombre de archivo slug-like
        filename = f"{datetime.now().strftime('%Y-%m-%d')}_{title.lower().replace(' ', '_')}.md"
        file_path = os.path.join(target_dir, filename)

        # 1. Crear el Nodo Markdown (Corregido: f-string con saltos de línea explícitos)
        header = f"---\ntitle: {title}\nscope: {scope}\nstatus: ACTIVO\ndate: {datetime.now().strftime('%Y-%m-%d')}\ntags: {tags}\n---\n\n"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(header + content)

        # 2. Actualizar el Índice
        node_entry = {
            "title": title,
            "path": f"SYSTEM/MEMORIA/Nodos_de_Conocimiento/{filename}" if scope == "terroir" else f"MIND/KNOWLEDGE/{filename}",
            "tags": tags,
            "distilled_knowledge": distilled,
            "status": "ACTIVO",
            "scope": scope
        }
        
        success, msg = update_index(target_index, node_entry)
        
        if success:
            print(json.dumps({
                "status": "success", 
                "message": f"Knowledge Node created and indexed in {scope}.",
                "file": file_path,
                "index_msg": msg
            }))
        else:
            print(json.dumps({"status": "partial_success", "message": f"Node created but index update failed: {msg}"}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()
