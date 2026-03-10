import os
import logging
import json
import uuid
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

logger = logging.getLogger(__name__)

class FrugalEmbeddingProvider:
    def __init__(self):
        self.model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

    def embed(self, text: str) -> List[float]:
        return [float(x) for x in list(self.model.embed([text]))[0]]

class ExocortexService:
    def __init__(self):
        if not QDRANT_URL:
            logger.error("QDRANT_URL no configurada en el entorno.")
            self.client = None
            return
            
        if QDRANT_URL.startswith("http"):
            self.client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY,
                prefer_grpc=False,
                check_compatibility=False
            )
        else:
            # Soporte para base de datos local (path-based)
            os.makedirs(QDRANT_URL, exist_ok=True)
            self.client = QdrantClient(path=QDRANT_URL)
            
        self.embedder = FrugalEmbeddingProvider()

    def recall(self, query: str, limit: int = 5, score_threshold: float = 0.5) -> List[Dict]:
        """Busqueda semantica usando query_points (API moderna 1.17+)."""
        if not self.client: return []
        try:
            q_vector = self.embedder.embed(query)
            
            # Usar query_points como metodo autoritativo para versiones nuevas
            res = self.client.query_points(
                collection_name=COLLECTION_NAME,
                query=q_vector,
                limit=limit,
                score_threshold=score_threshold,
                with_payload=True,
                timeout=30 # Aumentado para resiliencia en redes de trabajo
            ).points

            memories = []
            for point in res:
                # El objeto devuelto por query_points puede ser PointStruct o QueryResponse
                # pero el SDK lo estandariza en .points
                memories.append({
                    "text": point.payload.get("text", ""),
                    "score": point.score,
                    "metadata": {k: v for k, v in point.payload.items() if k != "text"}
                })
            return memories
        except Exception as e:
            logger.error(f"Error en recall semantico (query_points): {e}")
            return []

    def upsert_state(self, category: str, data: Dict):
        """Inyecta un elemento de estado en el SNC usando SDK oficial."""
        if not self.client: return
        try:
            custom_id = str(data.get("id") or str(uuid.uuid4()))
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, custom_id))
            text_to_embed = data.get("title") or data.get("summary") or "living state item"
            vector = self.embedder.embed(text_to_embed)

            self.client.upsert(
                collection_name="terroir_nervous_system",
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "category": category,
                            "original_id": custom_id,
                            "timestamp": datetime.now().isoformat(),
                            **data
                        }
                    )
                ]
            )
        except Exception as e:
            logger.error(f"SNC - Error inyectando estado: {e}")

    def update_signal(self, node_id: str, data: Dict):
        """Actualiza el semaforo de estado para un nodo especifico (cli/vigia)."""
        if not self.client: return
        try:
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"signal_{node_id}"))
            self.client.upsert(
                collection_name="terroir_nervous_system",
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=[0.0] * 384,
                        payload={
                            "node": node_id,
                            "timestamp": datetime.now().isoformat(),
                            **data
                        }
                    )
                ]
            )
        except Exception as e:
            logger.error(f"SNC - Error actualizando señal {node_id}: {e}")

    def get_signal(self, node_id: str) -> Optional[Dict]:
        """Recupera la ultima señal de un nodo."""
        if not self.client: return None
        try:
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"signal_{node_id}"))
            res = self.client.retrieve(
                collection_name="terroir_nervous_system",
                ids=[point_id]
            )
            if res: return res[0].payload
            return None
        except Exception as e:
            logger.error(f"SNC - Error obteniendo señal {node_id}: {e}")
            return None

    def get_living_thread(self) -> List[Dict]:
        """Recupera los ultimos turnos del hilo compartido."""
        if not self.client: return []
        try:
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, "living_thread_buffer"))
            res = self.client.retrieve(
                collection_name="terroir_nervous_system",
                ids=[point_id]
            )
            if res:
                return res[0].payload.get("turns", [])
            return []
        except Exception as e:
            logger.error(f"SNC - Error obteniendo hilo vivo: {e}")
            return []

    def push_to_living_thread(self, turn: Dict, max_turns: int = 50):
        """Añade un turno al hilo compartido y mantiene el buffer circular."""
        if not self.client: return
        try:
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, "living_thread_buffer"))
            current_turns = self.get_living_thread()
            
            # Añadir nuevo turno con timestamp si no lo tiene
            if "ts" not in turn:
                turn["ts"] = datetime.now().isoformat()
            
            current_turns.append(turn)
            
            # Mantener buffer circular (FIFO)
            if len(current_turns) > max_turns:
                current_turns = current_turns[-max_turns:]
            
            self.client.upsert(
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
        except Exception as e:
            logger.error(f"SNC - Error actualizando hilo vivo: {e}")

# Instancia Global
exocortex = ExocortexService()
