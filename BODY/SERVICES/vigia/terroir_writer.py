import os
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("terroir_writer")

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

class TerroirWriter:
    """
    Encargado de la 'Cosecha Fisica' de El Vigia.
    Transforma dialogos efimeros de Telegram en artefactos JSON persistentes.
    """
    
    def __init__(self, terroir_root=None):
        self.terroir_root = terroir_root or TerroirLocator.get_orchestrator_root()
        # Using TerroirLocator for Phenotype Discovery
        self.logs_dir = TerroirLocator.get_mem_root() / "logs_vigia"
        
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

    def write_interaction(self, session_id, user_id, user_name, prompt, response):
        """
        Registra una interaccion en el archivo de sesion correspondiente.
        """
        filename = f"vigia-{session_id}.json"
        filepath = os.path.join(self.logs_dir, filename)
        
        timestamp = datetime.now().isoformat()
        
        interaction = {
            "timestamp": timestamp,
            "user_id": user_id,
            "user_name": user_name,
            "prompt": prompt,
            "response": response
        }
        
        data = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                logger.error(f"Error leyendo log existente {filename}: {e}")
        
        data.append(interaction)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error escribiendo interaccion en {filename}: {e}")
            return False

    def generate_session_id(self, user_id):
        """Genera un ID unico para un hilo de conversacion."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{user_id}-{timestamp}"
