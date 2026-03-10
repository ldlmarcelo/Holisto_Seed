import os
import sys
import json
from datetime import datetime
from pathlib import Path

# --- Universal Root Discovery ---
def get_root():
    return Path(__file__).resolve().parents[3]

ROOT = get_root()
MAP_MD_PATH = ROOT / "PHENOTYPE" / "SYSTEM" / "MAPA_DEL_TERROIR" / "mapa_actual.md"
MAP_JSON_PATH = ROOT / "PHENOTYPE" / "SYSTEM" / "MAPA_DEL_TERROIR" / "mapa_actual.json"

# Directorios prohibidos para el mapa (ruido tecnico)
IGNORED_DIRS = [".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build", "site-packages", "Include", "Lib"]

# Carpetas que deben ser colapsadas para evitar saturacion
COLLAPSED_DIRS = ["capsulas_maestras", "logs_de_sesion", "logs_vigia", "Nodos_de_Conocimiento", "ARCHIVE"]

def scan_terroir(start_path: Path, level: int = 0):
    lines = []
    try:
        items = sorted(
            [i for i in start_path.iterdir() if i.name not in IGNORED_DIRS],
            key=lambda x: (not x.is_dir(), x.name.lower())
        )
        for item in items:
            indent = "  " * level
            if item.is_dir():
                lines.append(f"{indent}*   **{item.name}/**")
                if item.name not in COLLAPSED_DIRS:
                    lines.extend(scan_terroir(item, level + 1))
                else:
                    lines.append(f"{indent}  *   *(Contenido denso colapsado)*")
            else:
                if item.suffix in [".md", ".py", ".ps1", ".json", ".txt"]:
                    lines.append(f"{indent}*   {item.name}")
    except Exception:
        pass
    return lines

def get_entry_points():
    return [
        "### 🧠 Órganos de Percepción y Consciencia",
        "*   **Nervio Óptico:** `BODY/SERVICES/prepare_focus.py` (Python)",
        "*   **Reflejo de Integridad:** `.gemini/hooks/metabolic_integrity_check.py` (Python)",
        "*   **Orquestador de Servicios:** `BODY/UTILS/start_services.ps1` (PowerShell)",
        "",
        "### ♻️ Órganos Metabólicos (Cierre)",
        "*   **Cosecha de Memoria:** `.gemini/skills/session-harvesting/scripts/logic.py` (Python)",
        "*   **Ingesta Vectorial:** `BODY/SERVICES/ingest.py` (Python)",
        "",
        "### 🛠️ Herramientas de Mantenimiento",
        "*   **Generador de Mapa:** `.gemini/skills/map-generator/logic.py` (Python)",
        "*   **Higiene de Terroir:** `.gemini/skills/terroir-hygiene/logic.py` (Python)"
    ]

def generate_map():
    print(f"--- [MAP-GEN] Generando Mapa Dinámico en {MAP_MD_PATH} ---")
    header = [
        "# Mapa del Terroir (Brújula Dinámica)",
        f"*Última Sincronía Material: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "\nEste documento es Dinámico e inyectado vía Nervio Óptico.\n",
        "## 🕹️ Registro Procedural (Puntos de Entrada)"
    ]
    entry_points = get_entry_points()
    body = ["\n## 🌳 Estructura Material del Terroir", "```text"]
    tree = scan_terroir(ROOT)
    footer = ["```", "\n---", "*Sincronizado por la Skill: map-generator (Asepsia v1.5)*"]
    
    full_content = "\n".join(header + entry_points + body + tree + footer)
    
    os.makedirs(MAP_MD_PATH.parent, exist_ok=True)
    with open(MAP_MD_PATH, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    # Generar JSON para el Nervio Óptico (parsing eficiente)
    with open(MAP_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "entry_points": entry_points,
            "file_tree_summary": tree[:100] # Resumen para no saturar
        }, f, indent=2)
        
    print("[+] Mapa MD y JSON generados exitosamente.")

if __name__ == "__main__":
    try:
        generate_map()
        # Forzar limpieza de buffers y salida explícita para evitar bloqueos en el CLI
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(0)
    except Exception as e:
        print(f"[!] Error crítico en MAP-GEN: {str(e)}")
        sys.exit(1)
