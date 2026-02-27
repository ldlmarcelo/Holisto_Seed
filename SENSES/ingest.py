import os
import uuid
import sys
import logging
import hashlib
import argparse
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
from fastembed import TextEmbedding

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

# --- Configuration ---
TERROIR_ROOT = TerroirLocator.get_orchestrator_root()
load_dotenv(TERROIR_ROOT / ".env")

try: import docx
except ImportError: docx = None
try: import fitz
except ImportError: fitz = None

MAINTENANCE_LOGS_DIR = TerroirLocator.get_logs_dir()
if not os.path.exists(MAINTENANCE_LOGS_DIR): os.makedirs(MAINTENANCE_LOGS_DIR)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("VECTOR_COLLECTION", "terroir_memory_frugal")
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE", "384"))

ALLOWED_EXTENSIONS = {
    '.md', '.txt', '.py', '.js', '.html', '.css', '.json',
    '.sh', '.ps1', '.yml', '.yaml', '.xml', '.sql', '.env.example',
    '.docx', '.pdf'
}

def is_ignored(path: str) -> bool:
    """Filtro Gourmet: Elimina ruido tecnico y personal."""
    norm_path = path.replace("\\", "/").lower()
    filename = os.path.basename(norm_path)
    parts = norm_path.split("/")
    
    FORBIDDEN_DIRS = {
        '.git', '.venv', '.gemini', '__pycache__', 'node_modules', 
        '.idea', '.vscode', 'venv', 'dist', 'build', 'snapshots',
        'logs_mantenimiento', 'tmp', 'shared' # 'shared' es zona de intercambio manual
    }
    FORBIDDEN_FILES = {
        'package-lock.json', 'yarn.lock', 'composer.lock', 
        '__init__.py', '.gitignore', '.gitmodules', 'license', 
        'requirements.txt', 'ultimo_reporte_ingesta.json'
    }

    if filename in FORBIDDEN_FILES: return True
    if any(filename.endswith(ext) for ext in ['.map', '.min.js', '.min.css']): return True
    for part in parts:
        if part in FORBIDDEN_DIRS or (part.startswith('.') and part not in {'.', '..', '.env.example'}):
            return True
    return False

log_file = os.path.join(MAINTENANCE_LOGS_DIR, f"ingest_deep_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file, encoding='utf-8'), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ingest")

class FrugalEmbeddingProvider:
    def __init__(self):
        model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
        logger.info(f"Cargando motor local {model_name}...")
        self.model = TextEmbedding(model_name=model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        valid_texts = [t if t.strip() else "vacio" for t in texts]
        return [list(emb) for emb in self.model.embed(valid_texts)]

def setup_collection(client: QdrantClient, force_recreate: bool = False):
    try:
        exists = client.collection_exists(COLLECTION_NAME)
        if exists and force_recreate:
            logger.warning(f"Recreando coleccion {COLLECTION_NAME}...")
            try:
                client.delete_collection(COLLECTION_NAME)
                exists = False
            except Exception as e:
                if "403" in str(e):
                    logger.warning("Permiso denegado para borrar coleccion. Limpiando puntos existentes...")
                    for t in ["artifact", "artifact_chunk"]:
                        client.delete(COLLECTION_NAME, points_selector=models.Filter(must=[models.FieldCondition(key="type", match=models.MatchValue(value=t))]))
                else: raise e

        if not exists:
            logger.info(f"Creando coleccion {COLLECTION_NAME} ({VECTOR_SIZE}d)...")
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE)
            )
        
        for field in ["file_path", "type"]:
            client.create_payload_index(COLLECTION_NAME, field_name=field, field_schema=models.PayloadSchemaType.KEYWORD)
    except Exception as e:
        logger.error(f"Error en setup de Qdrant: {e}")

def calculate_hash(filepath: str) -> str:
    md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""): md5.update(chunk)
        return md5.hexdigest()
    except: return "hash_error"

class RecursiveFrugalSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", " ", ""]

    def split_text(self, text: str) -> List[str]:
        return self._recursive_split(text, self.separators)

    def _recursive_split(self, text: str, separators: List[str]) -> List[str]:
        final_chunks = []
        separator = separators[-1]
        new_separators = []
        for i, _s in enumerate(separators):
            if _s == "": separator = _s; break
            if _s in text:
                separator = _s
                new_separators = separators[i+1:]
                break
        splits = text.split(separator) if separator != "" else list(text)
        good_splits = []
        for s in splits:
            if len(s) < self.chunk_size: good_splits.append(s)
            else:
                if good_splits: final_chunks.extend(self._merge_splits(good_splits, separator)); good_splits = []
                if not new_separators: final_chunks.append(s[:self.chunk_size])
                else: final_chunks.extend(self._recursive_split(s, new_separators))
        if good_splits: final_chunks.extend(self._merge_splits(good_splits, separator))
        return final_chunks

    def _merge_splits(self, splits: List[str], separator: str) -> List[str]:
        chunks, current_doc, total = [], [], 0
        for s in splits:
            _len = len(s) + (len(separator) if current_doc else 0)
            if total + _len > self.chunk_size and total > 0:
                chunks.append(separator.join(current_doc))
                while total > self.chunk_overlap or (total > 0 and total + _len > self.chunk_size):
                    popped = current_doc.pop(0)
                    total -= len(popped) + len(separator)
            current_doc.append(s)
            total += _len
        if current_doc: chunks.append(separator.join(current_doc))
        return chunks

def get_stable_id(rel_path: str, chunk_index: int, chunk_content: str) -> str:
    content_hash = hashlib.md5(chunk_content.encode('utf-8')).hexdigest()
    norm_path = rel_path.replace("\\", "/").lower()
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{norm_path}-{chunk_index}-{content_hash}"))

def get_ontology_circle(rel_path: str) -> str:
    norm = rel_path.replace("\\", "/").lower()
    if any(x in norm for x in ["memoria", "memory", "constitucion"]): return "intimate_self"
    if any(x in norm for x in ["biblioteca", "library"]): return "proximal_you"
    return "functional_body"

def clean_biographic_content(log_data: dict) -> str:
    narrative = []
    for msg in log_data.get("messages", []):
        m_type = msg.get("type")
        content = msg.get("content", "")
        text = " ".join([p["text"] if isinstance(p, dict) else p for p in (content if isinstance(content, list) else [content])]).strip()
        if m_type == "user": narrative.append(f"USER: {text}")
        elif m_type == "gemini": narrative.append(f"HOLISTO: {text}")
    return "\n\n".join(narrative)

def read_and_chunk_content(filepath: str) -> List[Dict[str, Any]]:
    ext = os.path.splitext(filepath)[1].lower()
    splitter = RecursiveFrugalSplitter()
    try:
        if os.path.getsize(filepath) > 50 * 1024 * 1024: return []
        content = ""
        if ext == '.json':
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                try:
                    data = json.load(f)
                    content = clean_biographic_content(data) if "messages" in data else json.dumps(data, indent=2, ensure_ascii=False)
                except: f.seek(0); content = f.read()
        elif ext == '.docx' and docx:
            doc = docx.Document(filepath)
            content = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        elif ext == '.pdf' and fitz:
            doc = fitz.open(filepath)
            content = "".join([page.get_text() for page in doc])
        else:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f: content = f.read()
        return [{"text": t, "chunk_index": i} for i, t in enumerate(splitter.split_text(content))] if content.strip() else []
    except Exception as e:
        logger.error(f"Error procesando {filepath}: {e}"); return []

def scan_terroir() -> List[Dict]:
    docs = []
    root_path = TerroirLocator.get_orchestrator_root()
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d))]
        for file in files:
            full_path = os.path.join(root, file)
            if is_ignored(full_path) or os.path.splitext(file)[1].lower() not in ALLOWED_EXTENSIONS: continue
            rel_path = os.path.relpath(full_path, root_path)
            docs.append({"path": full_path, "rel_path": rel_path, "hash": calculate_hash(full_path), "circle": get_ontology_circle(rel_path), "filename": file})
    return docs

def process_ingest(client: QdrantClient, embedder: FrugalEmbeddingProvider, batch_size: int = 20):
    all_docs = scan_terroir()
    if not all_docs: return
    
    file_hash_map = {}
    try:
        logger.info("Mapeando el estado actual de la memoria en la nube...")
        next_offset = None
        while True:
            res, next_offset = client.scroll(collection_name=COLLECTION_NAME, limit=1000, offset=next_offset, with_payload=["file_hash", "file_path"])
            for p in res:
                path = p.payload.get("file_path")
                fhash = p.payload.get("file_hash")
                if path: file_hash_map[path] = fhash
            if not next_offset: break
        logger.info(f"Mapeo completado. Se reconocen {len(file_hash_map)} archivos en la nube.")
    except Exception as e: logger.warning(f"No se pudo mapear la coleccion previa: {e}")

    docs_to_process = [d for d in all_docs if d["hash"] != file_hash_map.get(d["rel_path"].replace("\\", "/"))]
    logger.info(f"Archivos escaneados: {len(all_docs)}. Archivos que requieren actualizacion: {len(docs_to_process)}")

    if not docs_to_process:
        logger.info("✨ Memoria perfectamente sincronizada."); return

    point_accumulator = []
    total_updated_chunks = 0
    for doc in docs_to_process:
        rel_path = doc["rel_path"].replace("\\", "/")
        logger.info(f"Actualizando: {rel_path}")
        chunks = read_and_chunk_content(doc["path"])
        if not chunks: continue

        if rel_path in file_hash_map:
            try: client.delete(COLLECTION_NAME, points_selector=models.Filter(must=[models.FieldCondition(key="file_path", match=models.MatchValue(value=rel_path))]))
            except: pass

        embeddings = embedder.embed([c["text"] for c in chunks])
        for i, emb in enumerate(embeddings):
            chunk = chunks[i]
            point_accumulator.append(models.PointStruct(id=get_stable_id(rel_path, chunk["chunk_index"], chunk["text"]), vector=emb, payload={"text": chunk["text"], "file_path": rel_path, "filename": doc["filename"], "file_hash": doc["hash"], "chunk_index": chunk["chunk_index"], "type": "artifact_chunk", "ontology_circle": doc["circle"], "last_updated": datetime.now().isoformat()}))
            if len(point_accumulator) >= batch_size:
                client.upsert(COLLECTION_NAME, point_accumulator)
                total_updated_chunks += len(point_accumulator); logger.info(f">>> UPSERT: {len(point_accumulator)} chunks subidos."); point_accumulator = []

    if point_accumulator:
        client.upsert(COLLECTION_NAME, point_accumulator)
        total_updated_chunks += len(point_accumulator); logger.info(f">>> FINAL UPSERT: {len(point_accumulator)} chunks subidos.")

    report = {"timestamp": datetime.now().isoformat(), "total_scanned": len(all_docs), "total_updated": len(docs_to_process), "total_chunks": total_updated_chunks}
    with open(os.path.join(MAINTENANCE_LOGS_DIR, "ultimo_reporte_ingesta.json"), "w", encoding='utf-8') as f: json.dump(report, f, indent=2)
    print(f"\n🍳 REPORTE FINAL: {len(all_docs)} escaneados, {len(docs_to_process)} actualizados, {total_updated_chunks} chunks.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reindex", action="store_true")
    args = parser.parse_args()
    try:
        parsed = urlparse(QDRANT_URL)
        client = QdrantClient(host=parsed.hostname or QDRANT_URL, port=parsed.port or (443 if "qdrant.io" in QDRANT_URL else 6333), https="qdrant.io" in QDRANT_URL, api_key=QDRANT_API_KEY, timeout=60)
        setup_collection(client, force_recreate=args.reindex)
        process_ingest(client, FrugalEmbeddingProvider())
    except Exception as e: logger.critical(f"Fallo critico: {e}")

if __name__ == "__main__": main()
