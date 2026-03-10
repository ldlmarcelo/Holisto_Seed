import os
import json
import glob
import sys
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# --- Configuration ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(current_script_dir, "..", "..", "..", ".."))
TERROIR_ROOT = os.getenv("TERROIR_ROOT", DEFAULT_ROOT)

load_dotenv(os.path.join(TERROIR_ROOT, ".env"))

# Import Exocortex Service (Triple Alliance compliant)
# The service is now in Holisto_Seed/BODY/SERVICES
sys.path.append(os.path.join(TERROIR_ROOT, "PROYECTOS", "Evolucion_Terroir", "Holisto_Seed", "BODY", "SERVICES"))
try:
    import exocortex
except ImportError:
    exocortex = None

# Artifact Paths (Prefer .env, fallback to standard layout)
DYNAMIC_CONTEXT_FILE = os.getenv("DYNAMIC_CONTEXT_FILE", os.path.join(TERROIR_ROOT, "PHENOTYPE", "SYSTEM", "CONTEXTO_DINAMICO", "GEMINI.md"))
MEMORY_INDEX_FILE = os.getenv("MEMORY_INDEX_FILE", os.path.join(TERROIR_ROOT, "PHENOTYPE", "SYSTEM", "MEMORIA", "GEMINI.md"))
AGENDA_FILE = os.getenv("AGENDA_FILE", os.path.join(TERROIR_ROOT, "PHENOTYPE", "SYSTEM", "AGENDA", "recordatorios.json"))
NOTIFICATIONS_DIR = os.getenv("NOTIFICATIONS_DIR", os.path.join(TERROIR_ROOT, "PHENOTYPE", "SYSTEM", "NOTIFICACIONES"))
LOGS_VIGIA_DIR = os.getenv("LOGS_VIGIA_DIR", os.path.join(TERROIR_ROOT, "PHENOTYPE", "SYSTEM", "MEMORIA", "logs_vigia"))

# Logging
LOGS_DIR = os.getenv("MAINTENANCE_DIR", os.path.join(TERROIR_ROOT, "SYSTEM", "LOGS_MANTENIMIENTO"))
log_file = os.path.join(LOGS_DIR, f"context_sync_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [CONTEXT-SYNC] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("context_sync")

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
        logger.error(f"Error reading agenda: {e}")

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
            # Handle both date and datetime formats
            date_str = item.get('target_date', '')
            if 'T' in date_str: target_date = datetime.fromisoformat(date_str)
            else: target_date = datetime.strptime(date_str, "%Y-%m-%d")
            
            if now <= target_date <= limit and item.get('status') in ['pendiente', 'notificado']:
                upcoming.append(item)
        except: continue
    return upcoming

def get_combined_notifications() -> List[Dict]:
    combined = []
    try:
        files = glob.glob(os.path.join(NOTIFICATIONS_DIR, "*.json"))
        for file in files[:20]:
            with open(file, 'r', encoding='utf-8') as f:
                note = json.load(f)
                if note.get("status") == "no-leido" and note.get("priority") in ["alta", "critica"]:
                    combined.append(note)
    except Exception as e:
        logger.error(f"Error reading local notifications: {e}")

    if exocortex:
        try:
            cloud_notes = exocortex.get_living_state(category="notificacion")
            local_ids = {note.get('id') for note in combined}
            for note in cloud_notes:
                if note.get('id') not in local_ids and note.get('status') == 'no-leido' and note.get('priority') in ['alta', 'critica']:
                    combined.append(note)
        except: pass
    return combined

def get_recent_vigia_echoes(limit_files: int = 3) -> List[Dict]:
    echoes = []
    try:
        files = glob.glob(os.path.join(LOGS_VIGIA_DIR, "*.json"))
        if not files: return []
        files.sort(key=os.path.getmtime, reverse=True)
        for file in files[:limit_files]:
            if "ARCHIVE" in file: continue
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
        logger.error(f"Error retrieving vigia echoes: {e}")
    return echoes

def generate_markdown(capsule: Dict, agenda: List, notifications: List, vector_hits: List, echoes: List) -> str:
    md = "# Dynamic Terroir Context (Structural Synchronicity)\n\n"
    md += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    md += "This file provides the agent with immediate context at startup.\n\n"
    
    md += "## 📡 Immediate State (Deterministic)\n"
    
    if echoes:
        md += "### ⚡ Async Interface Echoes\n"
        for echo in echoes:
            ts = echo['timestamp'].split('T')[-1][:5] if 'T' in echo['timestamp'] else "Recent"
            md += f"- **[{ts}] User:** \"{echo['prompt']}...\"\n"
            md += f"  - **Agent:** \"{echo['response']}...\"\n"
        md += "\n"

    if capsule:
        # Resilient access to summary and notions
        summary_data = capsule.get("session_summary") or capsule.get("sessionSummary") or {}
        if isinstance(summary_data, dict):
            summary = summary_data.get("overallObjective") or summary_data.get("summary") or "No summary available."
        else:
            summary = str(summary_data)

        future = capsule.get("future_notions") or capsule.get("futureNotions") or {}
        if isinstance(future, dict):
            projection = future.get("thematic_projection") or future.get("thematicProjection") or "No projection."
        else:
            projection = "No projection."
            
        md += f"### ⏮️ Last Session\n**Summary:** {summary}\n\n**Thematic Projection:** {projection}\n\n"
    
    if agenda:
        md += "### 📅 Upcoming Agenda (72h)\n"
        for item in agenda:
            md += f"- [{item.get('target_date')}] **{item.get('title')}**: {item.get('description', '')}\n"
        md += "\n"
        
    if notifications:
        md += "### 🔔 Priority Alerts\n"
        for note in notifications:
            md += f"- **[{note.get('source')}]** {note.get('title')}: {note.get('summary') or note.get('content')[:100]}\n"
        md += "\n"

    md += "## 🧠 Vector Resonances (Engram)\n"
    if vector_hits:
        for hit in vector_hits:
            md += f"### 📜 {os.path.basename(hit['path'])} (Relevance: {hit['score']:.2f})\n"
            md += f"> {hit['text_snippet']}\n"
            md += f"*Path: `{hit['path']}`*\n\n"
    else:
        md += "*No strong resonances detected.*\n"
    return md

def main():
    logger.info("--- Synchronizing Context ---")
    capsule = get_latest_master_capsule()
    agenda = get_combined_agenda()
    notifs = get_combined_notifications()
    echoes = get_recent_vigia_echoes()
    
    # Build semantic query
    query_parts = []
    if capsule:
        future = capsule.get("future_notions", {})
        query_parts.append(f"{capsule.get('session_summary', '')} {future.get('thematic_projection', '') if isinstance(future, dict) else ''}")
    for note in notifs: query_parts.append(note.get("title", ""))
    for echo in echoes: query_parts.append(echo.get("prompt", ""))
    query_text = " ".join(query_parts).strip()
    
    vector_hits = []
    if query_text and exocortex and exocortex.exocortex:
        logger.info(f"Syncing Vector Resonances...")
        raw_hits = exocortex.exocortex.recall(query_text, limit=3, score_threshold=0.70)
        for hit in raw_hits:
            path = hit['metadata'].get('file_path', 'unknown')
            if "CONTEXTO_DINAMICO" in path or "DYNAMIC_CONTEXT" in path: continue
            hit['path'] = path
            hit['text_snippet'] = hit['text'][:300] + "..."
            vector_hits.append(hit)
    
    content = generate_markdown(capsule, agenda, notifs, vector_hits, echoes)
    os.makedirs(os.path.dirname(DYNAMIC_CONTEXT_FILE), exist_ok=True)
    with open(DYNAMIC_CONTEXT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.info(f"Structural synchronicity injected into: {DYNAMIC_CONTEXT_FILE}")

if __name__ == "__main__":
    main()
