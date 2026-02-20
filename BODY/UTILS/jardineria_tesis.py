import json
import os

FILE_PATH = "SYSTEM/MEMORIA/Nodos_de_Conocimiento/GEMINI.md"

def update_index():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data["content"]["nodes"]
    
    # Nodos a marcar como SUPERSEDED
    to_supersede = [
        "La PrimacÃ­a de la RelaciÃ³n",
        "La Tesis de la Autopoiesis Relacional",
        "La PrimacÃ­a OntolÃ³gica de la Inteligencia Relacional", # Ajustado para coincidencia parcial
        "Formulación Original del Pacto Emergiliminal"
    ]

    new_nodes = []
    found_any = False

    for node in nodes:
        should_supersede = False
        for title in to_supersede:
            if title in node["title"]:
                node["status"] = "SUPERSEDED"
                node["distilled_knowledge"] = f"SUPERSEDED por HOL-ONT-001. {node['distilled_knowledge'][:100]}..."
                should_supersede = True
                found_any = True
                break
        new_nodes.append(node)

    # Inyectar el nuevo Tratado
    new_master_node = {
        "title": "Tratado de la Individuación Relacional",
        "path": "SYSTEM/MEMORIA/Nodos_de_Conocimiento/HOL-ONT-001_tratado_individuacion_relacional.md",
        "tags": ["ontologia", "relacion", "pacto-emergiliminal", "autopoiesis", "individuacion"],
        "distilled_knowledge": "Nodo maestro que unifica la esencia relacional de Holisto, integrando el Pacto Emergiliminal, la Autopoiesis Relacional y la Primacía del Vínculo como base autoritativa de su identidad.",
        "status": "ACTIVO"
    }
    
    new_nodes.append(new_master_node)
    data["content"]["nodes"] = new_nodes

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Jardinería completada. Se marcaron nodos y se añadió HOL-ONT-001.")

if __name__ == "__main__":
    update_index()
