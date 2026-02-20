import os
import argparse
import json
import sys
from pathlib import Path

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa si el PYTHONPATH no esta configurado
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

def create_skill(name, description, seed_path, orchestrator_path):
    # 1. Definir rutas (Using Path objects for robustness)
    skill_seed_dir = Path(seed_path) / "BODY" / "SKILLS" / name
    skill_scripts_dir = os.path.join(skill_seed_dir, "scripts")
    
    if os.path.exists(skill_seed_dir):
        print(f"Error: La skill '{name}' ya existe en la Semilla.")
        return

    # 2. Crear directorios
    os.makedirs(skill_scripts_dir, exist_ok=True)

    # 3. Generar SKILL.md con YAML correcto
    skill_md_content = f"""---
name: {name}
description: {description}
---

# Skill: {name.replace('-', ' ').title()}

## 🛠️ Lógica de Ejecución
Describir aquí la función del nuevo órgano.

## 🚀 Comando de Ejecución
```bash
python .gemini/skills/{name}/scripts/logic.py
```
"""
    with open(os.path.join(skill_seed_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md_content)

    # 4. Generar manifest.json
    manifest = {
        "name": name,
        "version": "1.0.0",
        "description": description,
        "entrypoint": f"scripts/logic.py"
    }
    with open(os.path.join(skill_seed_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    # 5. Generar esqueleto logic.py
    logic_content = """import sys
import json

def main():
    # Leer entrada de stdin si es necesario
    # input_data = sys.stdin.read()
    
    print(json.dumps({"status": "ok", "message": "Nueva skill ejecutada"}))

if __name__ == "__main__":
    main()
"""
    with open(os.path.join(skill_scripts_dir, "logic.py"), "w", encoding="utf-8") as f:
        f.write(logic_content)

    print(f"Éxito: Skill '{name}' creada en la Semilla.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de Skills de Holisto")
    parser.get_default("name")
    parser.add_argument("--name", required=True, help="Nombre de la skill (kebab-case)")
    parser.add_argument("--desc", required=True, help="Descripción breve")
    
    args = parser.parse_args()
    
    # Rutas base (Using TerroirLocator for Agnosticism)
    seed_root = TerroirLocator.get_seed_root()
    orchestrator_root = TerroirLocator.get_orchestrator_root()
    
    create_skill(args.name, args.desc, seed_root, orchestrator_root)
