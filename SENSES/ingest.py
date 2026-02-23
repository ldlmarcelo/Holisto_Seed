import os
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
ALLOWED_EXTENSIONS = {
    '.md', '.txt', '.py', '.js', '.html', '.css', '.json',
    '.sh', '.ps1', '.yml', '.yaml', '.xml', '.sql', '.env.example',
    '.docx', '.pdf'
}

MAX_FILE_SIZE_BYTES = int(os.getenv("MAX_INGEST_SIZE", str(5 * 1024 * 1024))) # 5 MB

def is_ignored(path: str) -> bool:
    """Verifica si la ruta debe ser ignorada (solo carpetas de sistema/cache)."""
    norm_path = path.replace("\\", "/").lower()
    parts = norm_path.split("/")
    
    # Bloqueo estricto por nombre de carpeta
    FORBIDDEN = {
        '.git', '.venv', '.gemini', '__pycache__', 'node_modules', 
        '.idea', '.vscode', 'venv', 'dist', 'build'
    }
    
    for part in parts:
        if part in FORBIDDEN:
            return True
        if part.startswith('.') and part not in {'.', '..'}:
            return True
                
    return False

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

def clean_biographic_content(log_data: dict) -> str:
    """Extrae solo la narrativa conversacional, eliminando ruido técnico."""
    narrative = []
    messages = log_data.get("messages", [])
    for msg in messages:
        m_type = msg.get("type")
        content = msg.get("content", "")
        
        text_parts = []
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    text_parts.append(part["text"])
                elif isinstance(part, str):
                    text_parts.append(part)
        elif isinstance(content, str):
            text_parts.append(content)
            
        clean_text = " ".join(text_parts).strip()
        if m_type == "user": narrative.append(f"USER: {clean_text}")
        elif m_type == "gemini": narrative.append(f"HOLISTO: {clean_text}")
            
    return "\n\n".join(narrative)

def read_content(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    try:
        file_size = os.path.getsize(filepath)
        LIMIT_RAW = 50 * 1024 * 1024 
        if file_size > LIMIT_RAW: return ""

        content = ""
        if ext == '.json':
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                try:
                    data = json.load(f)
                    if "messages" in data: content = clean_biographic_content(data)
                    else: content = json.dumps(data, indent=2)
                except: content = ""
        elif ext == '.docx' and docx:
            doc = docx.Document(filepath)
            content = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        elif ext == '.pdf' and fitz:
            doc = fitz.open(filepath)
            content = "".join([page.get_text() for page in doc])
        else:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        
        return content[:5000] if content else ""
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")
        return ""

def scan_terroir() -> List[Dict]:
    docs = []
    root_path = TerroirLocator.get_orchestrator_root()
    logger.info(f"--- START SCANNING from: {root_path} ---")
    
    for root, dirs, files in os.walk(root_path):
        for file in files:
            full_path = os.path.join(root, file)
            if is_ignored(full_path): continue
            
            ext = os.path.splitext(file)[1].lower()
            if ext not in ALLOWED_EXTENSIONS: continue
            
            rel_path = os.path.relpath(full_path, root_path)
            docs.append({
                "id": get_stable_id(rel_path),
                "path": full_path,
                "rel_path": rel_path,
                "hash": calculate_hash(full_path),
                "circle": get_ontology_circle(rel_path),
                "filename": file
            })
    return docs

def process_ingest(client: QdrantClient, embedder: FrugalEmbeddingProvider, batch_size: int):
    all_docs = scan_terroir()
    if not all_docs: return
    
    total_updated = 0
    total_scanned = len(all_docs)
    errors = []
    
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
            try:
                client.upsert(COLLECTION_NAME, points)
                total_updated += len(points)
                logger.info(f"Batch {i//batch_size + 1}: {len(points)} updates.")
            except Exception as e:
                logger.error(f"Error in batch {i//batch_size + 1}: {e}")
                errors.append(str(e))

    # --- Final Digestion Report ---
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_scanned": total_scanned,
        "updated_new": total_updated,
        "errors": errors
    }
    with open(os.path.join(MAINTENANCE_LOGS_DIR, "ultimo_reporte_ingesta.json"), "w", encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*40)
    print("🍳 REPORTE DE DIGESTIÓN SEMÁNTICA")
    print("="*40)
    print(f"Archivos Escaneados: {total_scanned}")
    print(f"Nuevas Nutriciones:  {total_updated}")
    print(f"Fricciones (Errores): {len(errors)}")
    print("="*40 + "\n")

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
            api_key=QDRANT_API_KEY,
            timeout=60
        )
        embedder = FrugalEmbeddingProvider()
        setup_collection(client, force_recreate=args.reindex)
        batch_size = 20
        process_ingest(client, embedder, batch_size)
    except Exception as e:
        logger.critical(f"Critical Failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
