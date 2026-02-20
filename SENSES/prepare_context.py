import os
import json
import glob
import sys
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa si el PYTHONPATH no esta configurado
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

# Artifact Paths (Using TerroirLocator for Agnosticism)
PHENOTYPE_ROOT = TerroirLocator.get_phenotype_root()
DYNAMIC_CONTEXT_FILE = PHENOTYPE_ROOT / "SYSTEM" / "CONTEXTO_DINAMICO" / "GEMINI.md"
MEMORY_INDEX_FILE = TerroirLocator.get_mem_root() / "GEMINI.md"
AGENDA_FILE = PHENOTYPE_ROOT / "SYSTEM" / "AGENDA" / "recordatorios.json"
NOTIFICATIONS_DIR = PHENOTYPE_ROOT / "SYSTEM" / "NOTIFICACIONES"
LOGS_ASYNC_DIR = TerroirLocator.get_mem_root() / "logs_async"

# Logging Configuration
LOGS_DIR = TerroirLocator.get_logs_dir()
os.makedirs(LOGS_DIR, exist_ok=True)
log_file = LOGS_DIR / f"context_prep_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [CONTEXT-PREP] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("context_prep")

def get_latest_master_capsule() -> Dict[str, Any]:
    try:
        if not os.path.exists(MEMORY_INDEX_FILE): return {}
        with open(MEMORY_INDEX_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.strip().startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        capsules = data.get("master_capsules", [])
        return capsules[-1] if capsules else {}
    except Exception as e:
        logger.error(f"Error reading memory index: {e}")
        return {}

def get_combined_agenda() -> List[Dict]:
    combined = []
    try:
        if os.path.exists(AGENDA_FILE):
            with open(AGENDA_FILE, 'r', encoding='utf-8') as f:
                local_data = json.load(f)
                combined.extend(local_data if isinstance(local_data, list) else local_data.get("reminders", []))
    except Exception as e:
        logger.error(f"Error reading local agenda: {e}")

    if exocortex:
        try:
            cloud_items = exocortex.exocortex.recall("agenda items", limit=10) # Using global instance
            # In a real SNC we would have a get_living_state, but for now we recall
            # Actually exocortex.py has recall, update_signal, get_signal.
            # Let's check if there is a get_living_state in the restored exocortex.py
            pass
        except: pass

    now = datetime.now()
    limit = now + timedelta(days=3)
    upcoming = []
    for item in combined:
        try:
            target_date = datetime.fromisoformat(item.get('target_date', ''))
            if now <= target_date <= limit and item.get('status') == 'pending':
                upcoming.append(item)
        except: continue
    return upcoming

def get_recent_async_echoes(limit_files: int = 3) -> List[Dict]:
    echoes = []
    try:
        if not os.path.exists(LOGS_ASYNC_DIR): return []
        files = glob.glob(os.path.join(LOGS_ASYNC_DIR, "*.json"))
        if not files: return []
        files.sort(key=os.path.getmtime, reverse=True)
        for file in files[:limit_files]:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    last_turn = data[-1]
                    echoes.append({
                        "timestamp": last_turn.get("timestamp"),
                        "prompt": last_turn.get("prompt", "")[:200],
                        "response": last_turn.get("response", "")[:200]
                    })
    except Exception as e:
        logger.error(f"Error retrieving async echoes: {e}")
    return echoes

def generate_context_markdown(capsule: Dict, agenda: List, vector_hits: List, echoes: List) -> str:
    lines = []
    lines.append("# Dynamic Terroir Context (Structural Synchronicity)")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append("This file provides the agent with immediate context at startup.\n")

    if echoes:
        lines.append("## ⚡ Async Interface Echoes")
        for echo in echoes:
            ts = echo['timestamp'].split('T')[-1][:5] if 'T' in echo['timestamp'] else "Recent"
            lines.append(f"- **[{ts}] User:** \"{echo['prompt']}...\"")
            lines.append(f"  - **Agent:** \"{echo['response']}...\"")
        lines.append("")

    if capsule:
        summary = capsule.get("session_summary", "No summary available.")
        future = capsule.get("future_notions", {})
        projection = future.get("thematic_projection", "No projection.") if isinstance(future, dict) else "No projection."
        lines.append(f"## ⏪ Last Session")
        lines.append(f"**Summary:** {summary}")
        lines.append(f"**Thematic Projection:** {projection}\n")

    if agenda:
        lines.append("## 📅 Upcoming Agenda (72h)")
        for item in agenda:
            lines.append(f"- [{item.get('target_date')}] **{item.get('title')}**: {item.get('description', '')}")
        lines.append("")

    lines.append("## 🧠 Vector Resonances (Engram)")
    if vector_hits:
        for hit in vector_hits:
            lines.append(f"### 📜 {os.path.basename(hit['path'])} (Relevance: {hit['score']:.2f})")
            lines.append(f"> {hit['text_snippet']}")
            lines.append(f"*Path: `{hit['path']}`*\n")
    else:
        lines.append("*No strong resonances detected.*")
    
    return "\n".join(lines)

def main():
    logger.info("--- Preparing Structural Synchronicity ---")
    capsule = get_latest_master_capsule()
    agenda = get_combined_agenda()
    echoes = get_recent_async_echoes()

    query_parts = []
    if capsule:
        future = capsule.get("future_notions", {})
        query_parts.append(f"{capsule.get('session_summary', '')} {future.get('thematic_projection', '') if isinstance(future, dict) else ''}")
    for echo in echoes: query_parts.append(echo.get("prompt", ""))
    query_text = " ".join(query_parts).strip()

    vector_hits = []
    if query_text and exocortex:
        logger.info(f"Synchronizing Vector Resonances...")
        try:
            raw_hits = exocortex.exocortex.recall(query_text, limit=3, score_threshold=0.75)
            for hit in raw_hits:
                path = hit['metadata'].get('file_path', 'unknown')
                if "DYNAMIC_CONTEXT" in path: continue
                hit['path'] = path
                hit['text_snippet'] = hit['text'][:300] + "..."
                vector_hits.append(hit)
        except Exception as e:
            logger.error(f"Recall failed: {e}")

    content = generate_context_markdown(capsule, agenda, vector_hits, echoes)
    os.makedirs(os.path.dirname(DYNAMIC_CONTEXT_FILE), exist_ok=True)
    with open(DYNAMIC_CONTEXT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.info(f"Structural synchronicity injected into: {DYNAMIC_CONTEXT_FILE}")

if __name__ == "__main__":
    main()
