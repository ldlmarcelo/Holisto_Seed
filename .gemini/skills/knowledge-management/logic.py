import json
import os
import sys
from datetime import datetime

def get_paths():
    """Detecta las rutas de las capas de la Triple Alianza de forma agnóstica."""
    base_dir = os.getcwd()
    # El índice de sabiduría es el punto de anclaje de la verdad
    knowledge_index = os.path.join(base_dir, "MIND", "KNOWLEDGE", "INDICE_SABIDURIA.md")
    
    paths = {
        "terroir": os.path.join(base_dir, "PHENOTYPE", "SYSTEM", "MEMORIA", "Nodos_de_Conocimiento"),
        "seed": os.path.join(base_dir, "MIND", "KNOWLEDGE"),
        "index": knowledge_index
    }
    return paths

def main():
    try:
        # El input viene de stdin (invocación del agente)
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"status": "error", "message": "No input data provided."}))
            return

        params = json.loads(input_data)
        scope = params.get("scope", "terroir") 
        title = params.get("title")
        content = params.get("content")
        tags = params.get("tags", [])
        distilled = params.get("distilled", "Nodo de conocimiento autogenerado.")
        node_id = params.get("id")

        if not title or not content:
            print(json.dumps({"status": "error", "message": "Title and content are required."}))
            return

        paths = get_paths()
        target_dir = paths.get(scope)
        if not target_dir:
            print(json.dumps({"status": "error", "message": f"Invalid scope: {scope}"}))
            return

        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        # Lógica de nombrado: HOL para Seed, TER para Terroir
        prefix = "HOL" if scope == "seed" else "TER"
        sub_type = params.get("type", "ONT") # Por defecto Ontología
        
        # Si no se provee ID, se genera uno secuencial
        if not node_id:
            existing_files = [f for f in os.listdir(target_dir) if f.startswith(f"{prefix}-{sub_type}")]
            count = len(existing_files) + 1
            node_id = f"{prefix}-{sub_type}-{count:03d}"
        
        # Nombre de archivo basado en ID y título (más robusto contra acentos)
        safe_title = title.lower().replace(' ', '_').replace(':', '').replace('/', '').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
        filename = f"{node_id}_{safe_title}.md"
        file_path = os.path.join(target_dir, filename)

        # Crear el Nodo Markdown con Frontmatter estándar
        header = f"---\nid: {node_id}\ntitle: {title}\ntags: {tags}\nstatus: ACTIVO\nscope: {scope}\n---\n\n"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(header + content)

        # Actualizar el Índice de Sabiduría (JSON)
        index_path = paths["index"]
        index_updated = False
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            # Ruta relativa para el índice (usando forward slashes para compatibilidad)
            rel_path = os.path.relpath(file_path, os.getcwd()).replace("\\", "/")
            
            new_node = {
                "title": title,
                "path": rel_path,
                "tags": tags,
                "distilled_knowledge": distilled,
                "status": "ACTIVO",
                "scope": scope
            }
            
            # Evitar duplicados por ruta
            index_data["content"]["nodes"] = [n for n in index_data["content"]["nodes"] if n["path"] != rel_path]
            index_data["content"]["nodes"].append(new_node)
            
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=4, ensure_ascii=False)
            index_updated = True

        print(json.dumps({
            "status": "success", 
            "message": f"Knowledge Node {node_id} created in {scope}. Index updated: {index_updated}",
            "file": file_path,
            "id": node_id
        }))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    try:
        main()
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Fatal error: {str(e)}"}))
        sys.exit(1)
