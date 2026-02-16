import os
import glob
import uuid
import sys
import logging
import hashlib
import argparse
import json
from datetime import datetime
from typing import List, Dict, Tuple
from urllib.parse import urlparse
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
from fastembed import TextEmbedding

# --- Configuration ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Default root is 5 levels up if executed from Seed/BODY/SKILLS/...
# But we prioritize TERROIR_ROOT env var
DEFAULT_ROOT = os.path.abspath(os.path.join(current_script_dir, "..", "..", "..", ".."))
TERROIR_ROOT = os.getenv("TERROIR_ROOT", DEFAULT_ROOT)

load_dotenv(os.path.join(TERROIR_ROOT, ".env"))

# Optional Imports
try: import docx
except ImportError: docx = None
try: import fitz
except ImportError: fitz = None

# Maintenance Dirs
MAINTENANCE_DIR = os.getenv("MAINTENANCE_DIR", os.path.join(TERROIR_ROOT, "SYSTEM", "LOGS_MANTENIMIENTO"))
if not os.path.exists(MAINTENANCE_DIR): os.makedirs(MAINTENANCE_DIR)

# Qdrant Config
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") 
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "terroir_memory_frugal")
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE", "384"))

# Cache File
CACHE_FILE = os.path.join(MAINTENANCE_DIR, "ingest_state_cache.json")

# --- Ingestion Filters ---
IGNORED_DIRS = set(os.getenv("IGNORED_DIRS", ".git,.venv,.gemini,__pycache__,node_modules,dist,build,bin,obj,lib,include,share,storage,tmp,temp,logs,LOGS_MANTENIMIENTO,.idea,.vscode").split(","))

ALLOWED_EXTENSIONS = {
    '.md', '.txt', '.py', '.js', '.html', '.css', '.json', 
    '.sh', '.ps1', '.yml', '.yaml', '.xml', '.sql', '.env.example',
    '.docx', '.pdf'
}

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024 # 5 MB

# Logging
log_file = os.path.join(MAINTENANCE_DIR, f"ingest_deep_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [INGEST] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("ingest")

class FrugalEmbeddingProvider:
    def __init__(self):
        logger.info("Loading local model BAAI/bge-small-en-v1.5...")
        self.model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

    def embed(self, texts: List[str]) -> List[List[float]]:
        valid_texts = [t if t.strip() else "empty" for t in texts]
        return [list(emb) for emb in self.model.embed(valid_texts)]

def load_state_cache() -> Dict:
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except: return {}
    return {}

def save_state_cache(cache: Dict):
    try:
        with open(CACHE_FILE, "w", encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving cache: {e}")

def calculate_hash(filepath: str) -> str:
    md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5.update(chunk)
        return md5.hexdigest()
    except: return "hash_error"

def get_stable_id(rel_path: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, rel_path.replace("", "/").lower()))

def get_ontology_circle(rel_path: str) -> str:
    norm = rel_path.replace("", "/").lower()
    if "system/memoria" in norm or norm == "gemini.md": return "intimo_yo"
    if "system/biblioteca" in norm: return "proximo_tu"
    return "cuerpo_funcional"

def read_content(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    try:
        file_size = os.path.getsize(filepath)
        if ext == '.json':
            if file_size > 100 * 1024 * 1024: return ""
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                try:
                    data = json.load(f)
                    narrative = []
                    if isinstance(data, dict) and "messages" in data:
                        for msg in data["messages"]:
                            role = "Usuario" if msg.get("type") == "user" else "Holisto"
                            content = msg.get("content", "")
                            if content:
                                if len(content) > 10000: content = content[:10000] + "... [TRUNCATED]"
                                narrative.append(f"{role}: {content}")
                        content = "\n\n".join(narrative)
                    elif isinstance(data, list) and len(data) > 0 and "prompt" in data[0]:
                        for turn in data:
                            p, r = turn.get("prompt", ""), turn.get("response", "")
                            if len(p) > 10000: p = p[:10000] + "... [TRUNCATED]"
                            if len(r) > 10000: r = r[:10000] + "... [TRUNCATED]"
                            if p: narrative.append(f"User: {p}")
                            if r: narrative.append(f"Agent: {r}")
                        content = "\n\n".join(narrative)
                    else: content = json.dumps(data, indent=2)
                    return content if len(content.encode('utf-8')) <= MAX_FILE_SIZE_BYTES else ""
                except: return ""
        if file_size > MAX_FILE_SIZE_BYTES: return ""
        if ext == '.docx' and docx:
            doc = docx.Document(filepath)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        elif ext == '.pdf' and fitz:
            doc = fitz.open(filepath)
            return "".join([page.get_text() for page in doc])
        else:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")
        return ""

def scan_terroir(old_cache: Dict) -> Tuple[List[Dict], Dict]:
    docs = []
    new_cache = {}
    logger.info(f"Scanning Terroir at: {TERROIR_ROOT}")
    
    for root, dirs, files in os.walk(TERROIR_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith('.')]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in ALLOWED_EXTENSIONS or file.startswith('.'): continue
            
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, TERROIR_ROOT)
            if "logs" in rel_path.lower() and ext == ".log": continue 

            try:
                stat = os.stat(full_path)
                mtime = stat.st_mtime
                size = stat.st_size
            except: continue
            
            cached = old_cache.get(rel_path, {})
            if cached.get("mtime") == mtime and cached.get("size") == size:
                file_hash = cached.get("hash")
                ingested = cached.get("ingested", False)
            else:
                file_hash = calculate_hash(full_path)
                ingested = False 

            doc_info = {
                "id": cached.get("id") or get_stable_id(rel_path),
                "path": full_path,
                "rel_path": rel_path,
                "hash": file_hash,
                "circle": get_ontology_circle(rel_path),
                "filename": file,
                "mtime": mtime,
                "size": size,
                "ingested": ingested
            }
            docs.append(doc_info)
            new_cache[rel_path] = {
                "id": doc_info["id"],
                "hash": file_hash,
                "mtime": mtime,
                "size": size,
                "ingested": ingested
            }
            
    logger.info(f"Scan complete. Found {len(docs)} candidates.")
    return docs, new_cache

def process_ingest(client: QdrantClient, embedder: FrugalEmbeddingProvider):
    old_cache = load_state_cache()
    all_docs, next_cache = scan_terroir(old_cache)
    
    dirty_docs = [d for d in all_docs if not d["ingested"]]
    
    if not dirty_docs:
        logger.info("Terroir synced (Cache OK). No changes pending.")
        save_state_cache(next_cache)
        return

    logger.info(f"Detected {len(dirty_docs)} new or modified files. Starting update...")

    batch_size = 20
    for i in range(0, len(dirty_docs), batch_size):
        batch = dirty_docs[i : i + batch_size]
        ids = [d["id"] for d in batch]
        
        existing_map = {}
        try:
            points = client.retrieve(COLLECTION_NAME, ids, with_payload=True)
            existing_map = {p.id: p for p in points}
        except Exception as e:
            logger.warning(f"Qdrant batch error {i}: {e}")

        to_embed_docs, to_embed_texts = [], []

        for doc in batch:
            point = existing_map.get(doc["id"])
            if point and point.payload.get("file_hash") == doc["hash"]:
                next_cache[doc["rel_path"]]["ingested"] = True
                continue
            
            content = read_content(doc["path"])
            if content.strip():
                to_embed_docs.append(doc)
                to_embed_texts.append(content)
            else:
                next_cache[doc["rel_path"]]["ingested"] = True 

        if to_embed_docs:
            try:
                embeddings = embedder.embed(to_embed_texts)
                points = []
                for j, emb in enumerate(embeddings):
                    doc = to_embed_docs[j]
                    points.append(models.PointStruct(
                        id=doc["id"], vector=emb,
                        payload={
                            "text": to_embed_texts[j],
                            "file_path": doc["rel_path"],
                            "filename": doc["filename"],
                            "file_hash": doc["hash"],
                            "type": "artifact",
                            "ontology_circle": doc["circle"],
                            "last_updated": datetime.now().isoformat()
                        }
                    ))
                client.upsert(COLLECTION_NAME, points)
                for doc in to_embed_docs:
                    next_cache[doc["rel_path"]]["ingested"] = True
                print(f"Batch {i//batch_size + 1}: +{len(points)} docs.")
            except Exception as e:
                logger.error(f"Error in batch: {e}")

    save_state_cache(next_cache)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reindex", action="store_true", help="Clear collection and reindex all")
    args = parser.parse_args()
    try:
        parsed = urlparse(QDRANT_URL)
        client = QdrantClient(
            host=parsed.hostname or QDRANT_URL,
            port=parsed.port or (443 if "qdrant.io" in QDRANT_URL else 6333),
            https="qdrant.io" in QDRANT_URL,
            api_key=QDRANT_API_KEY
        )
        embedder = FrugalEmbeddingProvider()
        if args.reindex:
            logger.warning(f"Recreating collection {COLLECTION_NAME}...")
            client.delete_collection(COLLECTION_NAME)
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE)
            )
        process_ingest(client, embedder)
    except Exception as e:
        logger.critical(f"Critical Failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
