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
        "seed": os.path.join(base_dir, "PROYECTOS", "Evolucion_Terroir", "Holisto_Seed", "MIND", "KNOWLEDGE"),
        "seed_index": os.path.join(base_dir, "PROYECTOS", "Evolucion_Terroir", "Holisto_Seed", "MIND", "KNOWLEDGE", "GEMINI.md")
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
        scope = params.get("scope", "terroir") # default terroir
        title = params.get("title")
        content = params.get("content")
        tags = params.get("tags", [])

        if not title or not content:
            print(json.dumps({"status": "error", "message": "Title and content are required."}))
            return

        paths = get_paths()
        target_dir = paths[scope]

        # Crear nombre de archivo slug-like
        filename = f"{datetime.now().strftime('%Y-%m-%d')}_{title.lower().replace(' ', '_')}.md"
        file_path = os.path.join(target_dir, filename)

        # Crear el Nodo Markdown
        header = f"---\ntitle: {title}\nscope: {scope}\nstatus: ACTIVO\ndate: {datetime.now().strftime('%Y-%m-%d')}\ntags: {tags}\n---\n\n"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(header + content)

        print(json.dumps({
            "status": "success", 
            "message": f"Knowledge Node created in {scope}. Vector ingestion will index it automatically.",
            "file": file_path
        }))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    try:
        main()
        # Forzar limpieza de buffers y salida explícita para evitar bloqueos en el CLI
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Fatal error: {str(e)}"}))
        sys.exit(1)
