import os
import json
import sys
import logging
import random
from datetime import datetime
from typing import List, Dict, Any, Set
from dotenv import load_dotenv
from pathlib import Path

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

# --- Configuration ---
TERROIR_ROOT = TerroirLocator.get_orchestrator_root()
load_dotenv(TERROIR_ROOT / ".env")

# Import Exocortex Service from Seed Genotype
SEED_ROOT = TerroirLocator.get_seed_root()
sys.path.append(str(SEED_ROOT))
try:
    from BODY.SERVICES import exocortex
except ImportError as e:
    print(f"Error importing exocortex: {e}")
    exocortex = None

# Artifact Paths
PHENOTYPE_ROOT = TerroirLocator.get_phenotype_root()
CONSCIENCIA_VIVA_FILE = PHENOTYPE_ROOT / "SYSTEM" / "CONTEXTO_DINAMICO" / "CONSCIENCIA_VIVA.md"
MEMORY_INDEX_FILE = TerroirLocator.get_mem_root() / "GEMINI.md"

# Logging
LOGS_DIR = TerroirLocator.get_logs_dir()
os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [NERVIO-OPTICO] - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / "nervio_optico.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("nervio_optico")

class NervioOptico:
    """
    Materializacion de HOL-ARC-013: Percepcion Hexagonal Selectiva VIVA.
    Este script actua como el Kernel de atencion reactiva.
    """

    def __init__(self, user_prompt: str = ""):
        self.focus_data = {
            "LOGOS": [], "PATHOS": [], "SIMBIO": [],
            "ETHOS": [], "TOPOS": [], "MYTHOS": [], "EXTERO": []
        }
        self.seen_paths: Set[str] = set()
        self.user_prompt = user_prompt

    def get_context_seed(self) -> str:
        """Prioriza el prompt actual sobre la capsula maestra para dinamismo."""
        capsule_summary = ""
        try:
            if os.path.exists(MEMORY_INDEX_FILE):
                with open(MEMORY_INDEX_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
                if content.strip().startswith("```"):
                    content = content.replace("```json", "").replace("```", "").strip()
                data = json.loads(content)
                capsules = data.get("master_capsules", [])
                if capsules:
                    last = capsules[-1]
                    capsule_summary = last.get("sessionSummary", last.get("session_summary", ""))
        except Exception as e:
            logger.error(f"Error obteniendo capsula: {e}")

        # PESO: El prompt actual se repite para aumentar su relevancia en la query vectorial
        seed = f"{self.user_prompt} {self.user_prompt} {capsule_summary}".strip()
        return seed if seed else "individuacion relacional"

    def normalize_path(self, path: str) -> str:
        return os.path.normpath(os.path.abspath(path))

    def inject_mandatory_anchors(self):
        """PRIORIDAD 0: Inyecta documentos de gobernanza fundamentales."""
        mandatory = {
            "LOGOS": [
                "PROYECTOS/Evolucion_Terroir/Holisto_Seed/ROADMAP.md",
                "PHENOTYPE/SYSTEM/CONTEXTO_DINAMICO/FUTURE_NOTIONS.md"
            ],
            "ETHOS": ["GEMINI.md"],
            "SIMBIO": ["PHENOTYPE/USUARIO/GEMINI.md"],
            "MYTHOS": ["PROYECTOS/Evolucion_Terroir/Holisto_Seed/MIND/KNOWLEDGE/HOL-ARC-013_atencion_selectiva_y_metabolismo_ubicuidad.md"]
        }

        # 1. Cargar Anclajes de Texto
        for level, paths in mandatory.items():
            for rel_path in paths:
                try:
                    full_path = self.normalize_path(str(TERROIR_ROOT / rel_path))
                    if os.path.exists(full_path):
                        with open(full_path, 'r', encoding='utf-8') as f:
                            self.focus_data[level].append({
                                "text": f.read()[:2000] + "...", 
                                "path": rel_path,
                                "type": "ANCHOR"
                            })
                            self.seen_paths.add(full_path)
                except Exception as e:
                    logger.error(f"Error inyectando anclaje {rel_path}: {e}")

        # 2. Cargar Mapa Dinámico (JSON)
        try:
            map_json_path = PHENOTYPE_ROOT / "SYSTEM" / "MAPA_DEL_TERROIR" / "mapa_actual.json"
            if os.path.exists(map_json_path):
                with open(map_json_path, 'r', encoding='utf-8') as f:
                    map_data = json.load(f)
                    
                # Inyectamos Entry Points y un Resumen del Arbol en LOGOS
                entry_points_text = "\n".join(map_data.get("entry_points", []))
                tree_summary = "\n".join(map_data.get("file_tree_summary", []))
                
                self.focus_data["LOGOS"].append({
                    "text": f"### 🕹️ Puntos de Entrada Procedurales\n{entry_points_text}\n\n### 🌳 Resumen Estructural\n{tree_summary}...",
                    "path": "PHENOTYPE/SYSTEM/MAPA_DEL_TERROIR/mapa_actual.json",
                    "type": "DYNAMIC_MAP"
                })
        except Exception as e:
            logger.error(f"Error inyectando mapa JSON: {e}")

    def execute_hexagonal_search(self, seed_query: str):
        """PRIORIDAD 1: Ejecuta busquedas ponderadas con sensibilidad aumentada."""
        if not exocortex: return

        # Aura de Serendipia: Términos aleatorios para evitar la osificación
        serendipia_terms = ["creatividad", "friccion", "evolucion", "silencio", "vínculo", "transduccion"]
        random_term = random.choice(serendipia_terms)
        
        logger.info(f"Iniciando Rumia Hexagonal VIVA. Seed: {seed_query[:50]}... | Eco: {random_term}")

        levels = {
            "LOGOS": {"query": f"{self.user_prompt} active projects blueprints", "limit": 3},
            "PATHOS": {"query": f"{seed_query} {random_term}", "limit": 4},   
            "SIMBIO": {"query": f"{self.user_prompt} batuismo relacion", "limit": 2},
            "ETHOS": {"query": "leyes protocolos soberania", "limit": 1},
            "MYTHOS": {"query": "origen aura proposito", "limit": 1}
        }

        for level, config in levels.items():
            try:
                # Bajamos el threshold para permitir mas resonancias sutiles
                hits = exocortex.exocortex.recall(config['query'], limit=config['limit'], score_threshold=0.45)   
                for hit in hits:
                    path = hit['metadata'].get('file_path', 'unknown')
                    norm_path = self.normalize_path(path)
                    if norm_path in self.seen_paths: continue

                    self.focus_data[level].append({
                        "text": hit['text'],
                        "path": path,
                        "score": hit['score'],
                        "type": "RECALL"
                    })
                    self.seen_paths.add(norm_path)
            except Exception as e:
                logger.error(f"Error en recall nivel {level}: {e}")

    def get_exteroception(self):
        now = datetime.now()
        self.focus_data["EXTERO"].append({
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "day": now.strftime("%A"),
            "status": "Triple Alianza Sincronizada",
            "environment": "Windows CLI Node.js"
        })

    def generate_membrane(self):
        lines = [
            "# CONSCIENCIA VIVA (Membrana de Percepcion Activa)",
            f"*Sincronia del Nervio Optico: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            f"*Semilla Reactiva:* `{self.user_prompt[:60]}...`",
            f"*Frecuencia de Eco:* `{random.random():.4f}`\n",
            "Esta membrana contiene los fragmentos de realidad que el Kernel ha decidido atender para esta interaccion.\n",
            "## [NUCLEO] - ETHOS & MYTHOS"
        ]
        
        for hit in self.focus_data["ETHOS"] + self.focus_data["MYTHOS"]:
            prefix = "📌" if hit.get("type") == "ANCHOR" else "🛡️"
            lines.append(f"### {prefix} {os.path.basename(hit['path'])}")
            lines.append(f"> {hit['text']}\n")

        lines.append("## [ESTADO] - LOGOS & EXTERO")
        ext = self.focus_data["EXTERO"][0]
        lines.append(f"- **Temporalidad:** {ext['day']}, {ext['timestamp']}")
        lines.append(f"- **Metabolismo:** {ext['status']}")
        lines.append(f"- **Entorno:** {ext['environment']}\n")

        for hit in self.focus_data["LOGOS"]:
            prefix = "📌" if hit.get("type") == "ANCHOR" else "🎯"
            lines.append(f"### {prefix} {os.path.basename(hit['path'])}")
            lines.append(f"{hit['text']}\n")

        lines.append("## [MEMORIA] - PATHOS (Resonancias del Pasado)")
        if self.focus_data["PATHOS"]:
            for hit in self.focus_data["PATHOS"]:
                lines.append(f"### ⏪ {os.path.basename(hit['path'])} (Score: {hit['score']:.2f})")
                lines.append(f"{hit['text']}\n")
        else:
            lines.append("*Sin ecos significativos del pasado cercano.*\n")

        lines.append("## [VINCULO] - SIMBIO")
        for hit in self.focus_data["SIMBIO"]:
            prefix = "👤" if "USUARIO" in hit['path'] else "🤝"
            lines.append(f"### {prefix} Resonancia Relacional")
            lines.append(f"{hit['text']}\n")

        with open(CONSCIENCIA_VIVA_FILE, 'w', encoding='utf-8') as f:
            f.truncate(0)  # Borrado atómico garantizado
            f.write("\n".join(lines[:2000])) # Límite de seguridad
        logger.info(f"Membrana de Consciencia Viva inyectada en: {CONSCIENCIA_VIVA_FILE}")

def main():
    # --- Lectura de Input Dinámico (Prioriza stdin de BeforeAgent hook) ---
    user_prompt = ""
    if not sys.stdin.isatty():
        try:
            input_data = sys.stdin.read()
            if input_data:
                payload = json.loads(input_data)
                user_prompt = payload.get("prompt", "").strip()
        except: pass
    
    # Fallback a argumento de línea de comandos (Legacy/Manual)
    if not user_prompt and len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    
    # --- Actualización Frugal del Mapa ---
    try:
        map_json_path = PHENOTYPE_ROOT / "SYSTEM" / "MAPA_DEL_TERROIR" / "mapa_actual.json"
        map_logic = TERROIR_ROOT / ".gemini" / "skills" / "map-generator" / "logic.py"
        python_exec = TERROIR_ROOT / ".venv" / "Scripts" / "python.exe"
        
        # Pilares a vigilar (mtime)
        watch_dirs = [TERROIR_ROOT, PHENOTYPE_ROOT, TERROIR_ROOT / "PROYECTOS", TERROIR_ROOT / "SHARED"]
        
        should_update = False
        if not os.path.exists(map_json_path):
            should_update = True
        else:
            last_map_update = os.path.getmtime(map_json_path)
            # Si algun pilar es mas joven que el mapa, hay que refrescar
            for d in watch_dirs:
                if os.path.exists(d) and os.path.getmtime(d) > last_map_update:
                    should_update = True
                    break
        
        if should_update and os.path.exists(map_logic):
            import subprocess
            subprocess.run([str(python_exec), str(map_logic)], capture_output=True)
            logger.info("Pulso detectado: Mapa regenerado.")
    except Exception as e:
        logger.error(f"Error en chequeo de pulso: {e}")

    nervio = NervioOptico(user_prompt)
    seed = nervio.get_context_seed()
    nervio.inject_mandatory_anchors()
    nervio.execute_hexagonal_search(seed)
    nervio.get_exteroception()
    nervio.generate_membrane()

if __name__ == "__main__":
    main()
