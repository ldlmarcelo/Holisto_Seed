import os
import glob
import uuid
import sys
import logging
import hashlib
import argparse
import json
from datetime import datetime
from typing import List, Dict
from urllib.parse import urlparse
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
from fastembed import TextEmbedding

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

# Optional Imports for document processing
try: import docx
except ImportError: docx = None
try: import fitz
except ImportError: fitz = None

# Logs Directory
MAINTENANCE_LOGS_DIR = TerroirLocator.get_logs_dir()
if not os.path.exists(MAINTENANCE_LOGS_DIR): os.makedirs(MAINTENANCE_LOGS_DIR)

# Qdrant Config
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("VECTOR_COLLECTION", "terroir_memory_frugal")
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE", "384"))

# --- Ingestion Filters ---
IGNORED_DIRS = set(os.getenv("IGNORED_DIRS", ".git,.venv,.gemini,__pycache__,node_modules,dist,build,bin,obj,lib,include,share,storage,tmp,temp,logs,MAINTENANCE_LOGS,.idea,.vscode").split(","))

ALLOWED_EXTENSIONS = {
    '.md', '.txt', '.py', '.js', '.html', '.css', '.json',
    '.sh', '.ps1', '.yml', '.yaml', '.xml', '.sql', '.env.example',
    '.docx', '.pdf'
}

MAX_FILE_SIZE_BYTES = int(os.getenv("MAX_INGEST_SIZE", str(5 * 1024 * 1024))) # Default 5 MB

# Logging
log_file = os.path.join(MAINTENANCE_LOGS_DIR, f"ingest_deep_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("ingest")

class FrugalEmbeddingProvider:
    def __init__(self):
        model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
        logger.info(f"Loading local model {model_name}...")
        self.model = TextEmbedding(model_name=model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        valid_texts = [t if t.strip() else "empty" for t in texts]
        return [list(emb) for emb in self.model.embed(valid_texts)]

def setup_collection(client: QdrantClient, force_recreate: bool = False):
    try:
        exists = client.collection_exists(COLLECTION_NAME)
        if exists and force_recreate:
            logger.warning(f"Recreating collection {COLLECTION_NAME}...")
            client.delete_collection(COLLECTION_NAME)
            exists = False

        if not exists:
            logger.info(f"Creating collection {COLLECTION_NAME} ({VECTOR_SIZE}d)...")
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE)
            )
        else:
            info = client.get_collection(COLLECTION_NAME)
            if info.config.params.vectors.size != VECTOR_SIZE:
                raise ValueError(f"Dimension mismatch: Expected {VECTOR_SIZE}, Found {info.config.params.vectors.size}")
    except Exception as e:
        logger.error(f"Qdrant setup error: {e}")
        raise

def calculate_hash(filepath: str) -> str:
    md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5.update(chunk)
        return md5.hexdigest()
    except: return "hash_error"

def get_stable_id(rel_path: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, rel_path.replace("\\", "/").lower()))

def get_ontology_circle(rel_path: str) -> str:
    norm = rel_path.replace("\\", "/").lower()
    if "memoria" in norm or "memory" in norm or norm == "constitution.md": return "intimate_self"
    if "biblioteca" in norm or "library" in norm: return "proximal_you"
    return "functional_body"

def read_content(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    try:
        file_size = os.path.getsize(filepath)
        if ext == '.json':
            if file_size > 100 * 1024 * 1024: return ""
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                try:
                    data = json.load(f)
                    return json.dumps(data, indent=2)
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

def scan_terroir() -> List[Dict]:
    docs = []
    logger.info(f"Scanning from: {TERROIR_ROOT}")
    for root, dirs, files in os.walk(TERROIR_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith('.')]
        for file in files:
            if file.startswith('.'): continue
            ext = os.path.splitext(file)[1].lower()
            if ext not in ALLOWED_EXTENSIONS: continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, TERROIR_ROOT)
            docs.append({
                "id": get_stable_id(rel_path),
                "path": full_path,
                "rel_path": rel_path,
                "hash": calculate_hash(full_path),
                "circle": get_ontology_circle(rel_path),
                "filename": file
            })
    return docs

def process_ingest(client: QdrantClient, embedder: FrugalEmbeddingProvider):
    all_docs = scan_terroir()
    if not all_docs: return
    
    batch_size = 20
    for i in range(0, len(all_docs), batch_size):
        batch = all_docs[i : i + batch_size]
        ids = [d["id"] for d in batch]
        
        existing_map = {}
        try:
            points = client.retrieve(COLLECTION_NAME, ids, with_payload=True)
            existing_map = {p.id: p for p in points}
        except: pass

        to_embed_docs, to_embed_texts = [], []
        for doc in batch:
            point = existing_map.get(doc["id"])
            if not point or point.payload.get("file_hash") != doc["hash"]:
                content = read_content(doc["path"])
                if content.strip():
                    to_embed_docs.append(doc)
                    to_embed_texts.append(content)

        if to_embed_docs:
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
            logger.info(f"Batch {i//batch_size + 1}: {len(points)} updates.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reindex", action="store_true")
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
        setup_collection(client, force_recreate=args.reindex)
        process_ingest(client, embedder)
    except Exception as e:
        logger.critical(f"Critical Failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
