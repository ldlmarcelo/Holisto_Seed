import os
import json
import sys
import logging

def find_terroir_root(start_path: str) -> str:
    """Busca la raiz del Terroir detectando el archivo .env."""
    current = os.path.abspath(start_path)
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, ".env")):
            return current
        current = os.path.dirname(current)
    return os.path.abspath(os.path.join(start_path, "../../../.."))

def append_to_index(capsule_path):
    # Detect Phenotype Index
    terroir_root = find_terroir_root(os.path.dirname(__file__))
    index_path = os.path.join(terroir_root, "PHENOTYPE", "SYSTEM", "MEMORIA", "GEMINI.md")
    
    if not os.path.exists(index_path):
        print(f"Error: Memory index not found at {index_path}")
        return

    try:
        with open(capsule_path, 'r', encoding='utf-8') as f:
            capsule_data = json.load(f)
        
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        # Ensure correct ascending order: append to the end
        if "master_capsules" not in index_data:
            index_data["master_capsules"] = []
            
        index_data["master_capsules"].append(capsule_data)
        
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully anchored {capsule_data.get('session_id', 'unknown')} to memory index.")
    except Exception as e:
        print(f"Error anchoring capsule: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        append_to_index(sys.argv[1])
