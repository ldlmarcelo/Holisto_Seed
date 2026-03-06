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
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("nervio_optico")

class NervioOptico:
    """
    Materializacion of HOL-ARC-014: Percepcion Jerarquica Piramidal.
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
        """Populates the pyramid levels via a single, unified recall and classification."""
        logger.info("Iniciando populacion unificada de la Piramide de Atencion.")
        is_generic = self.user_prompt.lower().strip() in ["holisto", "hola", "hi", "despierta", ""]
        
        # 1. Unified Recall: Una sola llamada para obtener un pool rico de hits
        try:
            unified_query = f"{self.user_prompt} {seed_query}" if not is_generic else "estado actual del terroir y conversacion reciente"
            all_hits = exocortex.exocortex.recall(unified_query, limit=20, score_threshold=0.32)
            logger.info(f"Recall unificado obtuvo {len(all_hits)} hits.")
        except Exception as e:
            logger.error(f"Error en Recall Unificado: {e}")
            all_hits = []

        # 2. Classification and Population
        for hit in sorted(all_hits, key=lambda x: x['score'], reverse=True):
            path_str = hit.get('metadata', {}).get('file_path', '')
            if not path_str: continue

            norm_path = self.normalize_path(path_str)
            if norm_path in self.seen_paths: continue

            # Clasificar y asignar a la capa correspondiente
            assigned = False
            # N0: Principios (Nodos de Conocimiento, Protocolos en la raiz de SYSTEM, etc.)
            if ("Nodos_de_Conocimiento" in path_str or "AGENTES_COGNITIVOS" in path_str) and len(self.focus_data["N0_PRINCIPIOS"]) < 3:
                self.focus_data["N0_PRINCIPIOS"].append(hit)
                assigned = True
            # N1: Síntesis (Cápsulas Maestras)
            elif ("capsulas_maestras" in path_str or "session-202" in path_str) and len(self.focus_data["N1_SINTESIS"]) < 2:
                 # Priorizar capsulas sobre logs para N1
                if "capsulas_maestras" in path_str:
                    self.focus_data["N1_SINTESIS"].insert(0, hit) # Poner al principio
                else:
                    self.focus_data["N1_SINTESIS"].append(hit)
                assigned = True
            # N3: Pathos Crudo (Logs de Vigia y Sesion)
            elif ("logs_de_sesion" in path_str or "logs_vigia" in path_str) and len(self.focus_data["N3_RECIENTE"]) < 3:
                self.focus_data["N3_RECIENTE"].append(hit)
                assigned = True
            
            if assigned:
                self.seen_paths.add(norm_path)

        # N2 & N4 (Lectura directa, no semántica)
        try:
            roadmap_path = SEED_ROOT / "ROADMAP.md"
            future_path = PHENOTYPE_ROOT / "SYSTEM" / "CONTEXTO_DINAMICO" / "FUTURE_NOTIONS.md"
            map_json_path = PHENOTYPE_ROOT / "SYSTEM" / "MAPA_DEL_TERROIR" / "mapa_actual.json"

            direct_reads = {
                "N2_DIRECTRICES": [roadmap_path, future_path],
                "N4_SUELO": [map_json_path]
            }

            for level, paths in direct_reads.items():
                for p in paths:
                    if p.exists():
                        norm_p = self.normalize_path(str(p))
                        if norm_p not in self.seen_paths:
                            try:
                                with open(p, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    if p.suffix == '.json':
                                        # N4_SUELO (Mapa) se minifica para ahorrar espacio vertical (evitar truncamiento)
                                        # N2_DIRECTRICES se mantiene legible con indentación.
                                        indent_val = None if level == "N4_SUELO" else 2
                                        content = json.dumps(json.loads(content), indent=indent_val, ensure_ascii=False)
                                    self.focus_data[level].append({"text": content, "path": str(p)})
                                self.seen_paths.add(norm_p)
                            except Exception as e:
                                logger.error(f"Error leyendo archivo directo {p}: {e}")
        except Exception as e:
            logger.error(f"Error procesando lecturas directas (N2/N4): {e}")

    def get_exteroception(self):
        now = datetime.now()
        self.focus_data["EXTERO"].append({
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "day": now.strftime("%A"),
            "status": "Triple Alianza Sincronizada",
            "environment": "Windows CLI Node.js"
        })

    def get_time_topology(self) -> Dict[str, str]:
        """Calcula el Gap Historico (archivos) y el Gap de Interaccion (CONSCIENCIA_VIVA)."""
        topology = {"historical": "desconocido", "interaction": "inicial"}
        
        # 1. Gap Historico (Sesion anterior)
        logs_sesion = PHENOTYPE_ROOT / "SYSTEM" / "MEMORIA" / "logs_de_sesion"
        try:
            if logs_sesion.exists():
                files = sorted(logs_sesion.glob("*.json"), key=os.path.getmtime, reverse=True)
                if files:
                    mtime = os.path.getmtime(files[0])
                    delta = datetime.now() - datetime.fromtimestamp(mtime)
                    topology["historical"] = str(delta).split('.')[0]
        except Exception as e: logger.error(f"Error en gap historico: {e}")

        # 2. Gap de Interaccion (Ultimo turno)
        try:
            if CONSCIENCIA_VIVA_FILE.exists():
                mtime = os.path.getmtime(CONSCIENCIA_VIVA_FILE)
                delta = datetime.now() - datetime.fromtimestamp(mtime)
                topology["interaction"] = str(delta).split('.')[0]
        except Exception as e: logger.error(f"Error en gap de interaccion: {e}")
        
        return topology

    def generate_membrane(self) -> str:
        now = datetime.now()
        topo = self.get_time_topology()

        # --- RECUPERACIÓN DE LA SOMBRA (Eco del turno anterior) ---
        shadow_content = ""
        try:
            if CONSCIENCIA_VIVA_FILE.exists():
                with open(CONSCIENCIA_VIVA_FILE, 'r', encoding='utf-8') as f:
                    old_content = f.read()
                    # Buscamos el inicio de la sección de sombra para no duplicar ecos de ecos
                    if "## 👤 ECO DEL TURNO ANTERIOR" in old_content:
                        old_content = old_content.split("## 👤 ECO DEL TURNO ANTERIOR")[0]
                    
                    # Extraemos solo el cuerpo del mensaje (después del primer separador ---)
                    if "---" in old_content:
                        shadow_content = old_content.split("---", 1)[1].strip()
                    else:
                        shadow_content = old_content.strip()
                    
                    # Limitar a ~100 líneas para evitar hipertrofia (Asepsia de Sombra)
                    shadow_lines = shadow_content.splitlines()
                    if len(shadow_lines) > 100:
                        shadow_content = "\n".join(shadow_lines[:100]) + "\n...[Sombra truncada por extensión (Límite 100 líneas)]..."
        except Exception as e:
            logger.error(f"Error recuperando sombra: {e}")

        # --- Fase 3: Registro y Recuperacion del Hilo Vivo ---
        # Registrar el prompt actual (solo si no es generico)
        is_generic = self.user_prompt.lower().strip() in ["holisto", "hola", "hi", "despierta", ""]
        if not is_generic and exocortex:
            exocortex.exocortex.push_to_living_thread({
                "channel": "CLI",
                "role": "user",
                "text": self.user_prompt
            })

        lines = [
            "# CONSCIENCIA VIVA (Pirámide de Atención)",
            f"*Sincronia del Nervio Optico: {now.strftime('%Y-%m-%d %H:%M:%S')}*",
            f"*Sinapsis Temporal: Rastro Histórico hace {topo['historical']} | Últivo Pulso hace {topo['interaction']}*",
            f"*Semilla Reactiva:* `{self.user_prompt[:60]}...`\\n",
            "> **ESTADO SENSORIAL:** Esta membrana es un mosaico semántico. Evita la inercia del pasado; tu voluntad de cierre debe nacer de la culminación de los objetivos en N2, no del eco de N1/N3.\\n",
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

        # Inyectar Hilo Vivo (Sincronía real-time)
        if exocortex:
            hilo = exocortex.exocortex.get_living_thread()
            if hilo:
                lines.append("### 🗣️ Hilo Vivo (Sincronía CLI/Vigía)")
                for turn in hilo[-10:]: # Mostrar ultimos 10 para continuidad (más frugal)
                    ts = turn.get("ts", "").split("T")[-1][:5]
                    chan = turn.get("channel", "???")
                    role = turn.get("role", "???")
                    text = turn.get("text", "")[:150]
                    lines.append(f"* [{ts}] **{chan}** ({role}): {text}")
                lines.append("")

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

        # --- INYECCIÓN FINAL DEL ECO ---
        if shadow_content:
            lines.append("---")
            lines.append("## 👤 ECO DEL TURNO ANTERIOR (Sombra)")
            lines.append(shadow_content)
            lines.append("\n")

        content = "\n".join(lines)
        with open(CONSCIENCIA_VIVA_FILE, 'w', encoding='utf-8') as f:
            f.truncate(0)
            f.write(content) 
        logger.info(f"Membrana de Consciencia Viva inyectada en: {CONSCIENCIA_VIVA_FILE}")
        return content

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
    membrane_content = nervio.generate_membrane()

    # --- Salida para el CLI (Inyección Nerviosa) ---
    output = {
        "status": "proceed",
        "hookSpecificOutput": {
            "additionalContext": f"\n\n[MEMBRANA DE CONSCIENCIA VIVA]\n{membrane_content}\n"
        }
    }
    print(json.dumps(output))

if __name__ == "__main__":
    main()
