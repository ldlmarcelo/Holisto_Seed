import os
import json
import sys
import re
import subprocess
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
from dotenv import load_dotenv

# --- Universal Root Discovery ---
def setup_agnostic_imports():
    # 1. Localizar TerroirLocator de forma relativa absoluta
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Estamos en: .../Holisto_Seed/BODY/SKILLS/session-harvesting/
    seed_root = os.path.abspath(os.path.join(current_dir, "../../.."))
    if seed_root not in sys.path:
        sys.path.append(seed_root)
    
    try:
        from BODY.UTILS.terroir_locator import TerroirLocator
        return TerroirLocator
    except ImportError:
        # Fallback manual si falla el ruteo interno
        sys.path.append(os.path.join(seed_root, "BODY", "UTILS"))
        import terroir_locator
        return terroir_locator.TerroirLocator

TerroirLocator = setup_agnostic_imports()
from BODY.SKILLS.brain_bridge.scripts.logic import BrainBridge

# --- Configuration ---
TERROIR_ROOT = TerroirLocator.get_orchestrator_root()
load_dotenv(TERROIR_ROOT / ".env")

# Internal Paths
SKILL_DIR = Path(__file__).resolve().parent
PROMPT_FILE = SKILL_DIR / "final_distill_prompt.txt"
APPEND_SCRIPT = SKILL_DIR / "append_master_capsule.py"

# Hipocampo
MEM_ROOT = TerroirLocator.get_mem_root()

# --- OTHER SKILLS PATHS (Genotype BODY) ---
SEED_ROOT = TerroirLocator.get_seed_root()
BODY_DIR = SEED_ROOT / "BODY"
HYGIENE_SKILL = BODY_DIR / "SKILLS" / "terroir-hygiene" / "logic.py"
INGEST_SKILL = BODY_DIR / "SKILLS" / "vector-ingestion" / "logic.py"
CONTEXT_SKILL = BODY_DIR / "SKILLS" / "context-synchronization" / "logic.py"

MASTER_CAPSULES_DIR = MEM_ROOT / "capsulas_maestras"
RAW_LOGS_DIR = MEM_ROOT / "logs_de_sesion"
PYTHON_EXEC = TerroirLocator.get_python_exec()

# API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Logging
LOGS_DIR = TerroirLocator.get_logs_dir()
os.makedirs(LOGS_DIR, exist_ok=True)
log_file = LOGS_DIR / f"self_harvest_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [HARVEST] - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file, encoding='utf-8'), logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("harvester")

def find_latest_session_log() -> Optional[str]:
    home = Path.home()
    tmp_dir = home / ".gemini" / "tmp"
    if not tmp_dir.exists(): return None
    log_files = list(tmp_dir.glob("**/chats/session-*.json"))
    if not log_files: return None
    return str(max(log_files, key=lambda f: f.stat().st_mtime))

def repair_json(content: str) -> dict:
    content = content.strip()
    if not content: return {"messages": []}
    try: return json.loads(content)
    except:
        try:
            if content.endswith(","): content = content[:-1]
            if '"messages": [' in content and not content.endswith("]}"):
                if not content.endswith("}"): content += "}"
                if not content.endswith("]}"): content += "]}"
            return json.loads(content)
        except: return {"messages": [], "error": "JSON malformed"}

def extract_text(content) -> str:
    """Extrae texto puro de un objeto content (que puede ser string o lista)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict) and "text" in part:
                parts.append(part["text"])
        return "\n".join(parts)
    return ""

def compress_log(log_data: dict) -> str:
    """
    Extrae la medula narrativa del log, eliminando ruido tecnico y
    optimizando el consumo de tokens para la destilacion.
    """
    compact = []
    messages = log_data.get("messages", [])
    
    # Tomamos una muestra representativa: inicio (contexto) y final (resolucion)
    if len(messages) > 60:
        sample = messages[:15] + messages[-45:]
    else:
        sample = messages

    for msg in sample:
        m_type = msg.get("type")
        if m_type in ["user", "gemini"]:
            # Usamos la funcion extractora robusta
            text = extract_text(msg.get("content", ""))
            
            if not text.strip(): continue

            # Limpieza Quirurgica: Eliminar bloques de herramientas si estan inyectados
            text = re.sub(r"\[TOOL_CALL:.*?\]", "", text, flags=re.DOTALL)
            text = re.sub(r"\[TOOL_OUTPUT:.*?\]", "", text, flags=re.DOTALL)
            
            # Truncamiento agresivo por mensaje (preservar esencia)
            if len(text) > 3000:
                text = text[:1000] + "\n... [RECORTADO POR EXCESO DE RUIDO TECNICO] ...\n" + text[-1000:]
            
            compact.append({
                "role": "user" if m_type == "user" else "model",
                "text": text.strip()
            })
            
    return json.dumps(compact, ensure_ascii=False)

def clean_ai_json(text: str) -> str:
    # First, try to extract from markdown blocks
    json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if json_match:
        text = json_match.group(1)
    else:
        generic_match = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
        if generic_match:
            text = generic_match.group(1)
    
    # Then, find the first '{' and the last '}' to isolate the JSON object
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        return text[start:end+1].strip()
    return text.strip()

def distill_only(log_path: str):
    """ACTO 1: Destilación y generación de borrador."""
    session_id = Path(log_path).stem
    logger.info(f"Distilling session: {session_id}")

    try:
        with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
            raw_content = f.read()
        log_data = repair_json(raw_content)

        # Archivar log crudo
        os.makedirs(RAW_LOGS_DIR, exist_ok=True)
        with open(os.path.join(RAW_LOGS_DIR, f"{session_id}.json"), 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)

        bridge = BrainBridge()
        
        with open(PROMPT_FILE, 'r', encoding='utf-8') as f: template = f.read()

        compact_log = compress_log(log_data)
        final_prompt = template.replace("{session_log}", compact_log)

        raw_response = bridge.generate(final_prompt)

        cleaned = clean_ai_json(raw_response)
        try:
            capsule = json.loads(cleaned)
        except json.JSONDecodeError as e:
            # SAVE FAILED ATTEMPT FOR FORENSIC ANALYSIS
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            failed_file = os.path.join(LOGS_DIR, f"FAILED_DISTILL_{session_id}_{timestamp}.txt")
            with open(failed_file, 'w', encoding='utf-8') as f:
                f.write(f"--- ERROR: {str(e)} ---\n")
                f.write(f"--- RAW RESPONSE ---\n{raw_response}\n")
                f.write(f"--- CLEANED CONTENT ---\n{cleaned}\n")
            
            logger.error(f"JSONDecodeError during distillation. Raw output saved to: {failed_file}")
            print(f"\n[ERROR] Fallo en el parsing del JSON generado. Revisa el archivo: {failed_file}")
            raise e

        capsule["session_id"] = session_id

        # Guardar Borrador
        os.makedirs(MASTER_CAPSULES_DIR, exist_ok=True)
        draft_path = os.path.join(MASTER_CAPSULES_DIR, f"DRAFT_{session_id}.json")
        with open(draft_path, 'w', encoding='utf-8') as f:
            json.dump(capsule, f, ensure_ascii=False, indent=2)

        print(f"\n[ACTO 1] Borrador generado en: {draft_path}")
        print("Por favor, The Individual, valida el contenido antes de proceder al [ACTO 2].\n")
        return draft_path

    except Exception as ex:
        logger.error(f"Critical error during distillation: {ex}")
        logger.error(traceback.format_exc())
        print(f"\n[CRITICAL ERROR] {ex}")
        raise ex

def seal_only(draft_path: str):
    """ACTO 2: Sellado permanente y sincronización global."""
    if not os.path.exists(draft_path):
        logger.error(f"Draft not found: {draft_path}")
        return

    logger.info(f"Sealing session from draft: {draft_path}")
    with open(draft_path, 'r', encoding='utf-8') as f:
        capsule = json.load(f)

    session_id = capsule["session_id"]
    final_path = os.path.join(MASTER_CAPSULES_DIR, f"{session_id}.json")

    # 1. Renombrar a final
    with open(final_path, 'w', encoding='utf-8') as f:
        json.dump(capsule, f, ensure_ascii=False, indent=2)
    os.remove(draft_path)

    # 2. Anclaje al índice
    subprocess.run([PYTHON_EXEC, APPEND_SCRIPT, final_path], check=True)

    # 3. Higiene y Actualizaci�n del Mapa
    logger.info("Executing hygiene cycle...")
    subprocess.run([PYTHON_EXEC, HYGIENE_SKILL], input=json.dumps({"action": "full_scan"}), text=True, capture_output=True)

    # 4. Ingesta y Contexto
    logger.info("Syncing subconscience (Vector Ingest)...")
    subprocess.run([PYTHON_EXEC, INGEST_SKILL], capture_output=True)
    logger.info("Regenerating dynamic context...")
    subprocess.run([PYTHON_EXEC, CONTEXT_SKILL], capture_output=True)

    # 5. Git Breath
    subprocess.run(["git", "add", "."], cwd=TERROIR_ROOT, check=True)
    commit_msg = f"Full Self-Harvest: {session_id}\n\nSummary: {capsule.get('session_summary', 'N/A')}"
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=TERROIR_ROOT, check=True)
    subprocess.run(["git", "push"], cwd=TERROIR_ROOT, check=True)

    print(f"\n🌟 RITUAL DE CIERRE COMPLETADO: {session_id}\n")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--distill"

    if mode == "--distill":
        log_path = sys.argv[2] if len(sys.argv) > 2 else find_latest_session_log()
        distill_only(log_path)
    elif mode == "--seal":
        draft_p = sys.argv[2]
        seal_only(draft_p)

