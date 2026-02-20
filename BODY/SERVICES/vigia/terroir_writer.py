import os
import json
import logging
from datetime import datetime

logger = logging.getLogger("terroir_writer")

class TerroirWriter:
    """
    Encargado de la 'Cosecha Fisica' de El Vigia.
    Transforma dialogos efimeros de Telegram en artefactos JSON persistentes.
    """
    
    def __init__(self, terroir_root):
        self.terroir_root = terroir_root
        self.logs_dir = os.path.join(self.terroir_root, "PHENOTYPE", "SYSTEM", "MEMORIA", "logs_vigia")
        
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
