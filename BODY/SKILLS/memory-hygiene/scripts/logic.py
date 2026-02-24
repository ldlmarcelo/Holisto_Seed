import json
import os
import argparse
import sys

class MemoryHygieneManager:
    def __init__(self, active_memory_path=None, generational_memory_index_path=None):
        """
        Inicializa el gestor de higiene de memoria.
        Usa variables de entorno para rutas de memoria activa y generacional.
        """
        self.active_memory_path = active_memory_path or os.getenv(
            "The Individual_ACTIVE_MEMORY_FILE",
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "SYSTEM", "MEMORIA", "GEMINI.md"))
        )
        self.generational_memory_index_path = generational_memory_index_path or os.getenv(
            "The Individual_GENERATIONAL_MEMORY_INDEX",
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "SYSTEM", "MEMORIA", "GENERACIONES", "GEMINI.md"))
        )

    def _load_active_memory(self):
        if not os.path.exists(self.active_memory_path):
            return {"master_capsules": []}
        with open(self.active_memory_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_active_memory(self, data):
        with open(self.active_memory_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load_dream(self, dream_file_path):
        if not os.path.exists(dream_file_path):
            raise FileNotFoundError(f"Archivo de sueño no encontrado: {dream_file_path}")
        with open(dream_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def prune_by_dream(self, dream_file_path):
        """
        Poda las cápsulas maestras de la memoria activa que ya han sido consolidadas en un sueño.
        Retorna el número de cápsulas eliminadas.
        """
        dream_data = self._load_dream(dream_file_path)
            
        ids_consolidados = []
        # Primero, intentar desde la raíz (formato antiguo o si se incluye directamente)
        if dream_data.get("source_session_ids"):
            ids_consolidados.extend(dream_data["source_session_ids"])
        
        # Luego, buscar dentro de thematic_cores (formato actual de Sueños Generacionales)
        if dream_data.get("thematic_cores"):
            for core in dream_data["thematic_cores"]:
                ids_consolidados.extend(core.get("related_sessions", []))
            
        # Si sigue vacío, el sueño no es válido para poda o no contiene IDs
        if not ids_consolidados:
            print(f"ADVERTENCIA: No se encontraron 'source_session_ids' ni 'related_sessions' en el archivo de sueño {dream_file_path}. Abortando poda.")
            return 0

        active_memory = self._load_active_memory()
        capsulas_activas = active_memory.get("master_capsules", [])
        initial_count = len(capsulas_activas)
        
        capsulas_conservadas = [
            c for c in capsulas_activas
            if c.get("session_id") not in ids_consolidados
        ]
        
        deleted_count = initial_count - len(capsulas_conservadas)
        
        if deleted_count > 0:
            active_memory["master_capsules"] = capsulas_conservadas
            self._save_active_memory(active_memory)
            print(f"Memoria activa saneada. Eliminadas: {deleted_count} cápsulas.")
        else:
            print("No se encontraron cápsulas para podar.")
        
        return deleted_count

    def get_memory_stats(self):
        """
        Retorna estadísticas básicas de la memoria activa.
        """
        active_memory = self._load_active_memory()
        num_capsules = len(active_memory.get("master_capsules", []))
        return {"num_active_capsules": num_capsules}

if __name__ == "__main__":
    # Ejemplo de uso con argumentos
    parser = argparse.ArgumentParser(description="Skill para higiene de memoria.")
    parser.add_argument("--prune_by_dream", help="Ruta al archivo JSON de la Cápsula de Sueño para usar en la poda.")
    parser.add_argument("--get_stats", action="store_true", help="Obtener estadísticas de la memoria activa.")
    
    args = parser.parse_args()
    
    manager = MemoryHygieneManager()

    if args.prune_by_dream:
        print(f"Iniciando poda con sueño: {args.prune_by_dream}")
        try:
            deleted = manager.prune_by_dream(args.prune_by_dream)
            print(f"Cápsulas eliminadas: {deleted}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
    elif args.get_stats:
        stats = manager.get_memory_stats()
        print(f"Estadísticas de Memoria Activa: {stats}")
    else:
        print("Uso: python logic.py --prune_by_dream <ruta_a_sueno.json> OR python logic.py --get_stats")
