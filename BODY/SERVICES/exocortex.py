import os
import logging
import json
import uuid
import time
import requests
from datetime import datetime
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
from fastembed import TextEmbedding

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa si el PYTHONPATH no esta configurado
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

# --- Configuracion ---
TERROIR_ROOT = TerroirLocator.get_orchestrator_root()
load_dotenv(TERROIR_ROOT / ".env")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "terroir_memory_frugal")
ATTENTION_SERVER_URL = "http://127.0.0.1:8089/embed"

logger = logging.getLogger(__name__)

class FrugalEmbeddingProvider:
    """Proveedor de embeddings con fallback inteligente."""
    def __init__(self):
        self.model = None # Carga perezosa (lazy load)

    def _get_local_model(self):
        if self.model is None:
            logger.info("SNC - Cargando motor de embeddings local (Fallback)...")
            self.model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        return self.model

    def embed(self, text: str) -> List[float]:
        # Intento 1: Servidor de Atencion (Super rapido)
        try:
            res = requests.post(ATTENTION_SERVER_URL, json={"text": text}, timeout=2)
            if res.status_code == 200:
                return res.json()["vector"]
        except Exception:
            pass

        # Intento 2: Procesamiento Local (Resiliencia)
        model = self._get_local_model()
        return [float(x) for x in list(model.embed([text]))[0]]

class ExocortexService:
    """
    Servicio de Memoria Vectorial (Exocortex).
    Evolucion HOL-ARC-024: Politica de Conexiones Efimeras (Usar y Soltar).
    """
    def __init__(self):
        self.embedder = FrugalEmbeddingProvider()
        if not QDRANT_URL:
            logger.error("QDRANT_URL no configurada.")

    def _get_client(self) -> Optional[QdrantClient]:
        """Crea una conexion efimera a la base de datos."""
        if not QDRANT_URL: return None
        try:
            if QDRANT_URL.startswith("http"):
                return QdrantClient(
                    url=QDRANT_URL,
                    api_key=QDRANT_API_KEY,
                    prefer_grpc=False,
                    check_compatibility=False
                )
            else:
                # DB Local: Asegurar que el directorio existe
                os.makedirs(QDRANT_URL, exist_ok=True)
                return QdrantClient(path=QDRANT_URL)
        except Exception as e:
            raise e

    def _execute_with_retry(self, func, *args, **kwargs):
        """Ejecuta una operacion con reintentos si la DB esta bloqueada."""
        max_retries = 5
        delay = 0.5
        
        for i in range(max_retries):
            client = None
            try:
                client = self._get_client()
                if not client: return None
                return func(client, *args, **kwargs)
            except Exception as e:
                if "already accessed by another instance" in str(e) and i < max_retries - 1:
                    logger.warning(f"SNC - DB Bloqueada. Reintento {i+1}/{max_retries} en {delay}s...")
                    time.sleep(delay)
                    delay *= 2 
                    continue
                logger.error(f"SNC - Error en operacion: {e}")
                return None
            finally:
                if client:
                    try: client.close()
                    except: pass
                    del client

    def recall(self, query: str, limit: int = 5, score_threshold: float = 0.5) -> List[Dict]:
        def _recall(client, q, lim, threshold):
            q_vector = self.embedder.embed(q)
            res = client.query_points(
                collection_name=COLLECTION_NAME,
                query=q_vector,
                limit=lim,
                score_threshold=threshold,
                with_payload=True,
                timeout=30
            ).points
            memories = []
            for point in res:
                memories.append({
                    "text": point.payload.get("text", ""),
                    "score": point.score,
                    "metadata": {k: v for k, v in point.payload.items() if k != "text"}
                })
            return memories
        
        return self._execute_with_retry(_recall, query, limit, score_threshold) or []

    def upsert_state(self, category: str, data: Dict):
        def _upsert(client, cat, d):
            custom_id = str(d.get("id") or str(uuid.uuid4()))
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, custom_id))
            text_to_embed = d.get("title") or d.get("summary") or "living state item"
            vector = self.embedder.embed(text_to_embed)
            client.upsert(
                collection_name="terroir_nervous_system",
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "category": cat,
                            "original_id": custom_id,
                            "timestamp": datetime.now().isoformat(),
                            **d
                        }
                    )
                ]
            )
        self._execute_with_retry(_upsert, category, data)

    def update_signal(self, node_id: str, data: Dict):
        def _update(client, nid, d):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"signal_{nid}"))
            client.upsert(
                collection_name="terroir_nervous_system",
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=[0.0] * 384,
                        payload={
                            "node": nid,
                            "timestamp": datetime.now().isoformat(),
                            **d
                        }
                    )
                ]
            )
        self._execute_with_retry(_update, node_id, data)

    def get_signal(self, node_id: str) -> Optional[Dict]:
        def _get(client, nid):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"signal_{nid}"))
            res = client.retrieve(collection_name="terroir_nervous_system", ids=[point_id])
            return res[0].payload if res else None
        return self._execute_with_retry(_get, node_id)

    def get_living_thread(self) -> List[Dict]:
        """Expuesta publicamente para lecturas externas."""
        def _get_thread(client):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, "living_thread_buffer"))
            res = client.retrieve(collection_name="terroir_nervous_system", ids=[point_id])
            return res[0].payload.get("turns", []) if res else []
        return self._execute_with_retry(_get_thread) or []

    def push_to_living_thread(self, turn: Dict, max_turns: int = 50):
        def _push(client, t, m):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, "living_thread_buffer"))
            # Recuperar el hilo usando el mismo cliente ya abierto (evita deadlock)
            res = client.retrieve(collection_name="terroir_nervous_system", ids=[point_id])
            current_turns = res[0].payload.get("turns", []) if res else []
            
            if "ts" not in t: t["ts"] = datetime.now().isoformat()
            current_turns.append(t)
            if len(current_turns) > m: current_turns = current_turns[-m:]
            
            client.upsert(
                collection_name="terroir_nervous_system",
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=[0.0] * 384,
                        payload={
                            "node": "global_hilo",
                            "last_update": datetime.now().isoformat(),
                            "turns": current_turns
                        }
                    )
                ]
            )
        self._execute_with_retry(_push, turn, max_turns)

    def search(self, query: str) -> str:
        try:
            from BODY.UTILS.search_tavily import search as tavily_search
            return tavily_search(query)
        except Exception as e:
            logger.error(f"Exocortex - Error en búsqueda externa: {e}")
            return f"❌ Error en búsqueda externa: {str(e)}"

# Instancia Global
exocortex = ExocortexService()
