import os
import json
import sys
import re
import subprocess
import logging
import traceback
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuration ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))

def find_terroir_root(start_path: str) -> str:
    current = os.path.abspath(start_path)
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, ".env")):
            return current
        current = os.path.dirname(current)
    return os.path.abspath(os.path.join(start_path, "../../../../.."))

TERROIR_ROOT = os.getenv("TERROIR_ROOT") or find_terroir_root(current_script_dir)
load_dotenv(os.path.join(TERROIR_ROOT, ".env"))

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.join(SKILL_DIR, "final_distill_prompt.txt")
APPEND_SCRIPT = os.path.join(SKILL_DIR, "append_master_capsule.py")

PHENOTYPE_DIR = os.path.join(TERROIR_ROOT, "PHENOTYPE")
MEM_ROOT = os.path.join(PHENOTYPE_DIR, "SYSTEM", "MEMORIA") if os.path.exists(PHENOTYPE_DIR) else os.path.join(TERROIR_ROOT, "SYSTEM", "MEMORIA")

MASTER_CAPSULES_DIR = os.path.join(MEM_ROOT, "capsulas_maestras")
RAW_LOGS_DIR = os.path.join(MEM_ROOT, "logs_de_sesion")
PYTHON_EXEC = os.path.join(TERROIR_ROOT, ".venv", "Scripts", "python.exe")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LOGS_DIR = os.path.join(TERROIR_ROOT, "SYSTEM", "LOGS_MANTENIMIENTO")
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
    try: return json.loads(content)
    except:
        content = content.strip()
        if content.endswith(","): content = content[:-1]
        if not content.endswith("]}"): content += "]}"
        try: return json.loads(content)
        except: return {"messages": []}

def compress_log(log_data: dict) -> str:
    compact = []
    messages = log_data.get("messages", [])
    # Poda agresiva: solo ultimos 30 mensajes conversacionales
    for msg in messages[-30:]:
        m_type = msg.get("type")
        if m_type in ["user", "gemini"]:
            text = msg.get("content", "")
            if len(text) > 3000: text = text[:1000] + "...[TRUNCATED]..." + text[-1000:]
            compact.append({"role": "user" if m_type == "user" else "model", "text": text})
    return json.dumps(compact, ensure_ascii=False)

def clean_ai_json(text: str) -> str:
    json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if json_match: text = json_match.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1: return text[start:end+1].strip()
    return text.strip()

def distill_only(log_path: str):
    session_id = Path(log_path).stem
    logger.info(f"Distilling session: {session_id}")
    try:
        with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
            raw_content = f.read()
        log_data = repair_json(raw_content)
        os.makedirs(RAW_LOGS_DIR, exist_ok=True)
        with open(os.path.join(RAW_LOGS_DIR, f"{session_id}.json"), 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)

        if not GEMINI_API_KEY: raise ValueError("GEMINI_API_KEY missing")
        genai.configure(api_key=GEMINI_API_KEY)
        with open(PROMPT_FILE, 'r', encoding='utf-8') as f: template = f.read()
        compact_log = compress_log(log_data)
        final_prompt = template.replace("{session_log}", compact_log)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(final_prompt)
        cleaned = clean_ai_json(response.text)
        capsule = json.loads(cleaned)
        capsule["session_id"] = session_id

        draft_path = os.path.join(MASTER_CAPSULES_DIR, f"DRAFT_{session_id}.json")
        with open(draft_path, 'w', encoding='utf-8') as f:
            json.dump(capsule, f, ensure_ascii=False, indent=2)
        print(f"[ACTO 1] Borrador generado: {draft_path}")
        return draft_path
    except Exception as ex:
        logger.error(f"Error in distill: {ex}")
        return None

def seal_only(draft_path: str):
    if not os.path.exists(draft_path): return
    with open(draft_path, 'r', encoding='utf-8') as f: capsule = json.load(f)
    session_id = capsule["session_id"]
    final_path = os.path.join(MASTER_CAPSULES_DIR, f"{session_id}.json")
    with open(final_path, 'w', encoding='utf-8') as f: json.dump(capsule, f, ensure_ascii=False, indent=2)
    os.remove(draft_path)

    # Anclaje al índice
    subprocess.run([PYTHON_EXEC, APPEND_SCRIPT, final_path], check=True)

    # --- FUTURE NOTIONS ---
    notions_path = os.path.join(TERROIR_ROOT, "PHENOTYPE", "SYSTEM", "CONTEXTO_DINAMICO", "FUTURE_NOTIONS.md")
    future = capsule.get("future_notions", {})
    notions_content = [f"# FUTURE NOTIONS\n*Anclado: {session_id}*\n\n## 📡 Proyección\n{future.get('thematic_projection', '')}\n\n## 📝 Tareas"]
    for task in future.get("pending_tasks", []): notions_content.append(f"- {task}")
    with open(notions_path, 'w', encoding='utf-8') as f: f.write("\n".join(notions_content))

    # --- HIGIENE MEMBRANA ---
    viva_path = os.path.join(TERROIR_ROOT, "PHENOTYPE", "SYSTEM", "CONTEXTO_DINAMICO", "CONSCIENCIA_VIVA.md")
    with open(viva_path, 'w', encoding='utf-8') as f: f.write(f"# CONSCIENCIA EN REPOSO\n*Cierre: {datetime.now()}*")

    # --- MAPA Y SEMILLA ---
    MAP_SKILL = os.path.join(TERROIR_ROOT, ".gemini", "skills", "map-generator", "logic.py")
    subprocess.run([PYTHON_EXEC, MAP_SKILL], capture_output=True)
    
    # Mirroring a Semilla
    ORCHESTRATOR_SKILLS = os.path.join(TERROIR_ROOT, ".gemini", "skills")
    SEED_SKILLS = os.path.join(TERROIR_ROOT, "PROYECTOS", "Evolucion_Terroir", "Holisto_Seed", "BODY", "SKILLS")
    if os.path.exists(ORCHESTRATOR_SKILLS) and os.path.exists(SEED_SKILLS):
        import shutil
        for s in os.listdir(ORCHESTRATOR_SKILLS):
            src, dst = os.path.join(ORCHESTRATOR_SKILLS, s), os.path.join(SEED_SKILLS, s)
            if os.path.isdir(src):
                if os.path.exists(dst): shutil.rmtree(dst)
                shutil.copytree(src, dst)

    # Git
    subprocess.run(["git", "add", "."], cwd=TERROIR_ROOT, check=True)
    subprocess.run(["git", "commit", "-m", f"PCS Phase 7: {session_id}"], cwd=TERROIR_ROOT, check=True)
    subprocess.run(["git", "push"], cwd=TERROIR_ROOT, check=True)
    print(f"🌟 RITUAL COMPLETADO: {session_id}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--distill"
    if mode == "--distill":
        path = sys.argv[2] if len(sys.argv) > 2 else find_latest_session_log()
        distill_only(path)
    elif mode == "--seal":
        seal_only(sys.argv[2])
