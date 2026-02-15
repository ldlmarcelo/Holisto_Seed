import os
import json
import glob
import sys
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# --- Path Configuration ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(current_script_dir, ".."))

load_dotenv(os.path.join(BASE_DIR, ".env"))

# Import Exocortex Service (Assumes a standardized 'services' module)
sys.path.append(os.path.join(BASE_DIR, "DISTRIBUTED_CORE"))
try:
    from services import exocortex
except ImportError:
    exocortex = None

# Artifact Paths (Customizable via env)
DYNAMIC_CONTEXT_FILE = os.getenv("DYNAMIC_CONTEXT_FILE", os.path.join(BASE_DIR, "SYSTEM", "DYNAMIC_CONTEXT", "GEMINI.md"))
MEMORY_INDEX_FILE = os.getenv("MEMORY_INDEX_FILE", os.path.join(BASE_DIR, "SYSTEM", "MEMORY", "GEMINI.md"))
AGENDA_FILE = os.getenv("AGENDA_FILE", os.path.join(BASE_DIR, "SYSTEM", "AGENDA", "reminders.json"))
NOTIFICATIONS_DIR = os.getenv("NOTIFICATIONS_DIR", os.path.join(BASE_DIR, "SYSTEM", "NOTIFICATIONS"))
LOGS_ASYNC_DIR = os.getenv("LOGS_ASYNC_DIR", os.path.join(BASE_DIR, "SYSTEM", "MEMORY", "logs_async"))

# Logging Configuration
LOGS_DIR = os.getenv("LOGS_DIR", os.path.join(BASE_DIR, "SYSTEM", "MAINTENANCE_LOGS"))
log_file = os.path.join(LOGS_DIR, f"context_prep_{datetime.now().strftime('%Y%m%d')}.log")

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
            cloud_items = exocortex.get_living_state(category="agenda")
            local_ids = {str(item.get('id')) for item in combined if item.get('id')}
            for item in cloud_items:
                if str(item.get('id')) not in local_ids: combined.append(item)
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
    md = "# Dynamic Terroir Context (Structural Synchronicity)

"
    md += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"
    md += "This file provides the agent with immediate context at startup.

"

    if echoes:
        md += "## ⚡ Async Interface Echoes
"
        for echo in echoes:
            ts = echo['timestamp'].split('T')[-1][:5] if 'T' in echo['timestamp'] else "Recent"
            md += f"- **[{ts}] User:** "{echo['prompt']}..."
"
            md += f"  - **Agent:** "{echo['response']}..."
"
        md += "
"

    if capsule:
        summary = capsule.get("session_summary", "No summary available.")
        future = capsule.get("future_notions", {})
        projection = future.get("thematic_projection", "No projection.") if isinstance(future, dict) else "No projection."
        md += f"## ⏪ Last Session
**Summary:** {summary}

**Thematic Projection:** {projection}

"

    if agenda:
        md += "## 📅 Upcoming Agenda (72h)
"
        for item in agenda:
            md += f"- [{item.get('target_date')}] **{item.get('title')}**: {item.get('description', '')}
"
        md += "
"

    md += "## 🧠 Vector Resonances (Engram)
"
    if vector_hits:
        for hit in vector_hits:
            md += f"### 📜 {os.path.basename(hit['path'])} (Relevance: {hit['score']:.2f})
"
            md += f"> {hit['text_snippet']}
"
            md += f"*Path: `{hit['path']}`*

"
    else:
        md += "*No strong resonances detected.*
"
    return md

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
        raw_hits = exocortex.recall(query_text, limit=3, score_threshold=0.75)
        for hit in raw_hits:
            path = hit['metadata'].get('file_path', 'unknown')
            if "DYNAMIC_CONTEXT" in path: continue
            hit['path'] = path
            hit['text_snippet'] = hit['text'][:300] + "..."
            vector_hits.append(hit)

    content = generate_context_markdown(capsule, agenda, vector_hits, echoes)
    os.makedirs(os.path.dirname(DYNAMIC_CONTEXT_FILE), exist_ok=True)
    with open(DYNAMIC_CONTEXT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.info(f"Structural synchronicity injected into: {DYNAMIC_CONTEXT_FILE}")

if __name__ == "__main__":
    main()
