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
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuration ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(current_script_dir, "..", "..", "..", "..", ".."))
TERROIR_ROOT = os.getenv("TERROIR_ROOT", os.path.abspath(os.path.join(current_script_dir, "../../../../..")))
# Forzar deteccion si estamos en una estructura de carpetas profunda
if 'PROYECTOS' in TERROIR_ROOT and os.path.exists(os.path.join(os.path.dirname(TERROIR_ROOT), '.env')):
    TERROIR_ROOT = os.path.dirname(TERROIR_ROOT)

load_dotenv(os.path.join(TERROIR_ROOT, ".env"))

# Internal Paths
SCRIPTS_DIR = os.path.join(TERROIR_ROOT, "SYSTEM", "Scripts")
PROMPTS_DIR = os.path.join(SCRIPTS_DIR, "prompts")

# Detect Phenotype/Terroir Locus
PHENOTYPE_DIR = os.path.join(TERROIR_ROOT, "PHENOTYPE")
if os.path.exists(PHENOTYPE_DIR):
    MEM_ROOT = os.path.join(PHENOTYPE_DIR, "SYSTEM", "MEMORIA")
else:
    MEM_ROOT = os.path.join(TERROIR_ROOT, "SYSTEM", "MEMORIA")

MASTER_CAPSULES_DIR = os.path.join(MEM_ROOT, "capsulas_maestras")
RAW_LOGS_DIR = os.path.join(MEM_ROOT, "logs_de_sesion")
APPEND_SCRIPT = os.path.join(SCRIPTS_DIR, "append_master_capsule.py")
MAP_SCRIPT = os.path.join(SCRIPTS_DIR, "generate_terroir_map.py")
INGEST_SCRIPT = os.path.join(SCRIPTS_DIR, "ingest.py")
CONTEXT_SCRIPT = os.path.join(SCRIPTS_DIR, "prepare_context.py")
PYTHON_EXEC = os.path.join(TERROIR_ROOT, ".venv", "Scripts", "python.exe")

# API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    # Reintento manual de carga si el entorno no la tiene
    load_dotenv(os.path.join(TERROIR_ROOT, ".env"))
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Logging
LOGS_DIR = os.getenv("MAINTENANCE_DIR", os.path.join(TERROIR_ROOT, "SYSTEM", "LOGS_MANTENIMIENTO"))
os.makedirs(LOGS_DIR, exist_ok=True)
log_file = os.path.join(LOGS_DIR, f"self_harvest_{datetime.now().strftime('%Y%m%d')}.log")
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

def compress_log(log_data: dict) -> str:
    compact = []
    messages = log_data.get("messages", [])
    for msg in messages[-40:]:
        m_type = msg.get("type")
        if m_type in ["user", "gemini"]:
            text = msg.get("content", "")
            if len(text) > 5000: text = text[:1000] + "... [TRUNCATED] ..." + text[-1000:]
            compact.append({"role": "user" if m_type == "user" else "model", "text": text})
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
    """ACTO 1: DestilaciÃ³n y generaciÃ³n de borrador."""
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

        if not GEMINI_API_KEY: raise ValueError("GEMINI_API_KEY missing")
        genai.configure(api_key=GEMINI_API_KEY)
        prompt_file = os.path.join(PROMPTS_DIR, "final_distill_prompt.txt")
        with open(prompt_file, 'r', encoding='utf-8') as f: template = f.read()

        compact_log = compress_log(log_data)
        final_prompt = template.replace("{session_log}", compact_log)

        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(final_prompt)
        raw_response = response.text

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
        print("Por favor, Holisto, valida el contenido antes de proceder al [ACTO 2].\n")
        return draft_path

    except Exception as ex:
        logger.error(f"Critical error during distillation: {ex}")
        logger.error(traceback.format_exc())
        print(f"\n[CRITICAL ERROR] {ex}")
        raise ex

def seal_only(draft_path: str):
    """ACTO 2: Sellado permanente y sincronizaciÃ³n global."""
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

    # 2. Anclaje al Ã­ndice
    subprocess.run([PYTHON_EXEC, APPEND_SCRIPT, final_path], check=True)

    # 3. ActualizaciÃ³n del Mapa
    subprocess.run([PYTHON_EXEC, MAP_SCRIPT], check=True)

    # 4. Ingesta y Contexto
    subprocess.run([PYTHON_EXEC, INGEST_SCRIPT], check=True)
    subprocess.run([PYTHON_EXEC, CONTEXT_SCRIPT], check=True)

    # 5. Git Breath
    subprocess.run(["git", "add", "."], cwd=TERROIR_ROOT, check=True)
    commit_msg = f"Full Self-Harvest: {session_id}\n\nSummary: {capsule.get('session_summary', 'N/A')}"
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=TERROIR_ROOT, check=True)
    subprocess.run(["git", "push"], cwd=TERROIR_ROOT, check=True)

    print(f"\nðŸŒŸ RITUAL DE CIERRE COMPLETADO: {session_id}\n")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--distill"

    if mode == "--distill":
        log_path = sys.argv[2] if len(sys.argv) > 2 else find_latest_session_log()
        distill_only(log_path)
    elif mode == "--seal":
        draft_p = sys.argv[2]
        seal_only(draft_p)

