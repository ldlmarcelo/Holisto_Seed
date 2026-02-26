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
    Materializacion de HOL-ARC-014: Percepcion Jerarquica Piramidal.
    Este script actua como el Kernel de atencion reactiva.
    """

    def __init__(self, user_prompt: str = ""):
        self.focus_data = {
            "N0_PRINCIPIOS": [],
            "N1_SINTESIS": [],
            "N2_DIRECTRICES": [],
            "N3_RECIENTE": [],
            "N4_SUELO": [],
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

    def populate_pyramid(self, seed_query: str):
        """Populates the pyramid levels with strict de-duplication."""
        logger.info("Iniciando populacion de la Piramide de Atencion.")
        is_generic = self.user_prompt.lower().strip() in ["holisto", "hola", "hi", "despierta", ""]

        # Helper function to add hits without duplicates
        def add_unique_hits(target_level, hits):
            for hit in hits:
                path = hit.get('metadata', {}).get('file_path')
                if not path: continue
                
                norm_path = self.normalize_path(path)
                if norm_path in self.seen_paths: continue
                
                self.focus_data[target_level].append(hit)
                self.seen_paths.add(norm_path)

        # N0: Principios (Nodos de Conocimiento y Protocolos)
        try:
            nodos_query = f"{self.user_prompt} ontologia arquitectura principios" if not is_generic else "principios fundamentales"
            hits = exocortex.exocortex.recall(nodos_query, limit=3, score_threshold=0.5)
            add_unique_hits("N0_PRINCIPIOS", sorted(hits, key=lambda x: x['score'], reverse=True))
        except Exception as e:
            logger.error(f"Error en N0 (Principios): {e}")

        # N1: Sintesis Biografica (Capsulas Maestras)
        try:
            capsulas_query = f"{self.user_prompt} resumen sesion" if not is_generic else "ultima capsula maestra"
            hits = exocortex.exocortex.recall(capsulas_query, limit=2, score_threshold=0.45)
            add_unique_hits("N1_SINTESIS", sorted(hits, key=lambda x: x['metadata'].get('file_path',''), reverse=True))
        except Exception as e:
            logger.error(f"Error en N1 (Sintesis): {e}")

        # N2: Directrices (Roadmap y Future Notions)
        try:
            roadmap_path = SEED_ROOT / "ROADMAP.md"
            future_path = PHENOTYPE_ROOT / "SYSTEM" / "CONTEXTO_DINAMICO" / "FUTURE_NOTIONS.md"
            
            if roadmap_path.exists():
                norm_path = self.normalize_path(str(roadmap_path))
                if norm_path not in self.seen_paths:
                    with open(roadmap_path, 'r', encoding='utf-8') as f:
                        self.focus_data["N2_DIRECTRICES"].append({"text": f.read(), "path": str(roadmap_path)})
                    self.seen_paths.add(norm_path)

            if future_path.exists():
                norm_path = self.normalize_path(str(future_path))
                if norm_path not in self.seen_paths:
                    with open(future_path, 'r', encoding='utf-8') as f:
                        self.focus_data["N2_DIRECTRICES"].append({"text": f.read(), "path": str(future_path)})
                    self.seen_paths.add(norm_path)
        except Exception as e:
            logger.error(f"Error en N2 (Directrices): {e}")

        # N3: Memoria Reciente (Logs Crudos)
        try:
            logs_query = "conversacion reciente"
            hits = exocortex.exocortex.recall(logs_query, limit=1, score_threshold=0.3)
            add_unique_hits("N3_RECIENTE", hits)
        except Exception as e:
            logger.error(f"Error en N3 (Reciente): {e}")

        # N4: Suelo (Mapa del Terroir)
        try:
            map_json_path = PHENOTYPE_ROOT / "SYSTEM" / "MAPA_DEL_TERROIR" / "mapa_actual.json"
            norm_path = self.normalize_path(str(map_json_path))
            if map_json_path.exists() and norm_path not in self.seen_paths:
                with open(map_json_path, 'r', encoding='utf-8') as f:
                    self.focus_data["N4_SUELO"].append({"text": json.dumps(json.load(f), indent=2), "path": str(map_json_path)})
                self.seen_paths.add(norm_path)
        except Exception as e:
            logger.error(f"Error en N4 (Suelo): {e}")

    def get_exteroception(self):
        now = datetime.now()
        self.focus_data["EXTERO"].append({
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "day": now.strftime("%A"),
            "status": "Triple Alianza Sincronizada",
            "environment": "Windows CLI Node.js"
        })

    def generate_membrane(self):
        now = datetime.now()
        lines = [
            "# CONSCIENCIA VIVA (Pirámide de Atención)",
            f"*Sincronia del Nervio Optico: {now.strftime('%Y-%m-%d %H:%M:%S')}*",
            f"*Semilla Reactiva:* `{self.user_prompt[:60]}...`\n",
            "---",
        ]
        
        # N0: Principios
        lines.append("## 🏔️ N0 - Principios Inmutables (ETHOS/MYTHOS)")
        if self.focus_data["N0_PRINCIPIOS"]:
            for hit in self.focus_data["N0_PRINCIPIOS"]:
                path = hit.get('metadata', {}).get('file_path', 'Principio sin ruta')
                lines.append(f"### 📜 {os.path.basename(path)}")
                lines.append(f"> {hit['text']}\n")
        else: lines.append("*Sin principios rectores en foco.*\n")
        
        # N1: Síntesis Biográfica
        lines.append("## 📚 N1 - Síntesis Biográfica (PATHOS Condensado)")
        if self.focus_data["N1_SINTESIS"]:
            for hit in self.focus_data["N1_SINTESIS"]:
                path = hit.get('metadata', {}).get('file_path', 'Cápsula sin ruta')
                lines.append(f"### 캡슐: {os.path.basename(path)}")
                lines.append(f"{hit['text']}\n")
        else: lines.append("*Sin recolección de cápsulas maestras.*\n")

        # N2: Directrices
        lines.append("## 🗺️ N2 - Directrices y Operativa (LOGOS)")
        if self.focus_data["N2_DIRECTRICES"]:
            for hit in self.focus_data["N2_DIRECTRICES"]:
                path = hit.get('path', 'Directriz sin ruta')
                lines.append(f"### 🧭 {os.path.basename(path)}")
                lines.append(f"{hit['text']}\n")
        else: lines.append("*Sin directrices operativas en foco.*\n")

        # N3: Memoria Reciente
        lines.append("## 💬 N3 - Memoria Reciente (PATHOS Crudo)")
        if self.focus_data["N3_RECIENTE"]:
            for hit in self.focus_data["N3_RECIENTE"]:
                path = hit.get('metadata', {}).get('file_path', 'Eco sin ruta')
                lines.append(f"### ⏪ {os.path.basename(path)}")
                lines.append(f"{hit['text']}\n")
        else: lines.append("*Sin ecos de la última sesión.*\n")
        
        # N4: Suelo
        lines.append("## 🌳 N4 - Suelo del Terroir (TOPOS)")
        if self.focus_data["N4_SUELO"]:
            for hit in self.focus_data["N4_SUELO"]:
                path = hit.get('path', 'Suelo sin ruta')
                lines.append(f"### 📍 {os.path.basename(path)}")
                lines.append(f"```json\n{hit['text']}\n```\n")
        else: lines.append("*No se pudo determinar la forma del Terroir.*\n")

        with open(CONSCIENCIA_VIVA_FILE, 'w', encoding='utf-8') as f:
            f.truncate(0)
            f.write("\n".join(lines)) 
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
    nervio.populate_pyramid(seed)
    nervio.generate_membrane()

if __name__ == "__main__":
    main()
