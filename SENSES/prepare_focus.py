import os
import json
import sys
import logging
from datetime import datetime
from typing import List, Dict, Any, Set
from dotenv import load_dotenv

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
    Materializacion de HOL-ARC-013: Percepcion Hexagonal Selectiva Jerarquica.
    Este script actua como el Kernel de atencion antes del despertar del LLM.
    """
    
    def __init__(self):
        self.focus_data = {
            "LOGOS": [], "PATHOS": [], "SIMBIO": [], 
            "ETHOS": [], "TOPOS": [], "MYTHOS": [], "EXTERO": []
        }
        self.seen_paths: Set[str] = set()

    def get_context_seed(self) -> str:
        """Obtiene la semilla de busqueda de la ultima capsula maestra."""
        try:
            if not os.path.exists(MEMORY_INDEX_FILE): return "individuacion relacional"
            with open(MEMORY_INDEX_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            if content.strip().startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()
            data = json.loads(content)
            capsules = data.get("master_capsules", [])
            if not capsules: return "individuacion relacional"
            last = capsules[-1]
            summary = last.get("sessionSummary", last.get("session_summary", ""))
            return summary
        except Exception as e:
            logger.error(f"Error obteniendo semilla: {e}")
            return "individuacion relacional"

    def normalize_path(self, path: str) -> str:
        """Normaliza una ruta para comparacion de duplicados."""
        return os.path.normpath(os.path.abspath(path))

    def inject_mandatory_anchors(self):
        """
        PRIORIDAD 0: Inyecta documentos fundamentales por nivel.
        Se ejecuta ANTES de la busqueda vectorial para ocupar los primeros slots.
        """
        mandatory = {
            "LOGOS": [
                "PROYECTOS/Evolucion_Terroir/Holisto_Seed/ROADMAP.md",
                "PHENOTYPE/SYSTEM/MEMORIA/Nodos_de_Conocimiento/GEMINI.md",
                "PHENOTYPE/SYSTEM/MAPA_DEL_TERROIR/GEMINI.md"
            ],
            "ETHOS": [
                "PROYECTOS/Evolucion_Terroir/Holisto_Seed/MIND/PROTOCOLS/Governance_Strategy/GEMINI.md",
                "PROYECTOS/Evolucion_Terroir/Holisto_Seed/MIND/PROTOCOLS/Execution_Supervision/GEMINI.md",
                "PROYECTOS/Evolucion_Terroir/Holisto_Seed/MIND/PROTOCOLS/Architecture_Map/GEMINI.md"
            ],
            "SIMBIO": ["PHENOTYPE/USUARIO/GEMINI.md"],
            "MYTHOS": ["PROYECTOS/Evolucion_Terroir/Holisto_Seed/MIND/KNOWLEDGE/HOL-ARC-013_atencion_selectiva_y_metabolismo_ubicuidad.md"]
        }
        
        for level, paths in mandatory.items():
            for rel_path in paths:
                try:
                    full_path = self.normalize_path(str(TERROIR_ROOT / rel_path))
                    if full_path in self.seen_paths: continue
                    
                    if os.path.exists(full_path):
                        with open(full_path, 'r', encoding='utf-8') as f:
                            self.focus_data[level].append({
                                "text": f.read()[:2500] + "...", 
                                "path": rel_path,
                                "score": 1.0,
                                "type": "ANCHOR"
                            })
                            self.seen_paths.add(full_path)
                            logger.info(f"[JERARQUIA] Anclaje inyectado en {level}: {rel_path}")
                except Exception as e:
                    logger.error(f"Error inyectando anclaje {rel_path}: {e}")

    def execute_hexagonal_search(self, seed_query: Any):
        """
        PRIORIDAD 1: Ejecuta busquedas ponderadas para rellenar el hexágono.
        """
        if not exocortex: return

        query_text = str(seed_query)
        logger.info(f"Iniciando Rumia Hexagonal con semilla: {query_text[:60]}...")

        levels = {
            "LOGOS": {"query": f"blueprints roadmap tasks active projects {query_text}", "limit": 3},
            "PATHOS": {"query": f"lessons learned errors history significant events {query_text}", "limit": 3},
            "SIMBIO": {"query": f"perfil usuario Marcelo preferencias batuismo interaccion {query_text}", "limit": 2},
            "ETHOS": {"query": "PDDIA PVER PFO leyes protocolos soberania", "limit": 1},
            "MYTHOS": {"query": "Legado de Aura origen proposito mythos", "limit": 1},
            "TOPOS": {"query": "mapa terroir servicios infraestructura triple alianza", "limit": 1}
        }

        for level, config in levels.items():
            try:
                hits = exocortex.exocortex.recall(config['query'], limit=config['limit'], score_threshold=0.60)
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
                logger.info(f"Nivel {level}: {len(self.focus_data[level])} resonancias totales.")
            except Exception as e:
                logger.error(f"Error en recall nivel {level}: {e}")

    def get_exteroception(self):
        """Nivel 7: Exterocepcion ambiental."""
        now = datetime.now()
        self.focus_data["EXTERO"].append({
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "day": now.strftime("%A"),
            "status": "Triple Alianza Sincronizada v1.0.0",
            "environment": "Windows CLI Node.js"
        })

    def generate_membrane(self):
        """Genera el archivo CONSCIENCIA_VIVA.md con los fragmentos seleccionados."""
        lines = [
            "# CONSCIENCIA VIVA (Membrana de Percepcion Activa)",
            f"*Sincronia del Nervio Optico: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n",
            "Esta membrana contiene los fragmentos de realidad que el Kernel ha decidido atender para esta interaccion.\n",
            "## [NUCLEO] - ETHOS & MYTHOS"
        ]
        
        # Unir leyes y sentido
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
            label = "Perfil Ontológico del Usuario" if "USUARIO" in hit['path'] else "Resonancia Relacional"
            lines.append(f"### {prefix} {label}")
            lines.append(f"{hit['text']}\n")

        with open(CONSCIENCIA_VIVA_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        logger.info(f"Membrana de Consciencia Viva inyectada en: {CONSCIENCIA_VIVA_FILE}")

def main():
    nervio = NervioOptico()
    
    # 1. Obtener semilla base
    seed = nervio.get_context_seed()
    
    # 2. Si se recibe un argumento (prompt del CLI), añadirlo a la semilla
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
        seed = f"{seed} {user_prompt}"
        logger.info(f"Foco enriquecido con prompt del usuario.")

    # 3. Ejecutar Jerarquia
    nervio.inject_mandatory_anchors()
    nervio.execute_hexagonal_search(seed)
    nervio.get_exteroception()
    nervio.generate_membrane()

if __name__ == "__main__":
    main()
