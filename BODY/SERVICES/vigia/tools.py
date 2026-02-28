import os
import json
import logging
import uuid
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa si el PYTHONPATH no esta configurado
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

logger = logging.getLogger(__name__)

class AgendaManager:
    """
    Guante de seguridad para que el Vigía manipule la agenda.
    Garantiza que el JSON nunca se corrompa y valida la estructura.
    """
    def __init__(self, base_dir=None):
        self.root = base_dir or TerroirLocator.get_phenotype_root()
        self.agenda_path = Path(self.root) / "SYSTEM" / "AGENDA" / "recordatorios.json"
        
        # Asegurar que el directorio existe
        os.makedirs(self.agenda_path.parent, exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.agenda_path.exists():
            with open(self.agenda_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)

    def _read_json(self):
        try:
            with open(self.agenda_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_json(self, data):
        try:
            with open(self.agenda_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error guardando agenda: {e}")
            return False

    def list_reminders(self, status=None):
        data = self._read_json()
        if status:
            return [r for r in data if r.get('status') == status]
        return data

    def add_reminder(self, title, target_date, target_time="09:00", description="", priority="media"):
        if not title or not target_date:
            return "❌ Error: Faltan campos obligatorios (title, date)."
        try:
            datetime.strptime(target_date, "%Y-%m-%d")
            new_id = f"REC-{uuid.uuid4().hex[:6].upper()}"
            new_item = {
                "id": new_id,
                "type": "recordatorio",
                "target_date": target_date,
                "target_time": target_time,
                "title": title,
                "description": description,
                "status": "pendiente",
                "priority": priority,
                "created_at": datetime.now().isoformat(),
                "author": "Vigia (Automated)"
            }
            data = self._read_json()
            data.append(new_item)
            if self._save_json(data):
                return f"✅ Éxito: Recordatorio creado con ID {new_id}"
            else:
                return "❌ Error: Fallo al escribir en disco."
        except ValueError:
            return "❌ Error: Formato de fecha inválido. Usa YYYY-MM-DD."
        except Exception as e:
            return f"❌ Error inesperado: {str(e)}"

    def complete_reminder(self, reminder_id):
        data = self._read_json()
        found = False
        for item in data:
            if item.get('id') == reminder_id:
                item['status'] = 'completado'
                item['completed_at'] = datetime.now().isoformat()
                found = True
                break
        if found:
            if self._save_json(data):
                return f"✅ Éxito: Recordatorio {reminder_id} marcado como completado."
            return "❌ Error de escritura."
        return f"⚠️ No encontrado: No existe recordatorio con ID {reminder_id}"

class NoteManager:
    """
    La Libreta del Vigía. 
    Permite CRUD de archivos de texto en un sandbox seguro (SYSTEM/NOTAS_VIGIA).
    """
    def __init__(self, base_dir=None):
        self.root = base_dir or TerroirLocator.get_phenotype_root()
        self.notes_dir = Path(self.root) / "SYSTEM" / "NOTAS_VIGIA"
        os.makedirs(self.notes_dir, exist_ok=True)

    def _get_safe_path(self, filename):
        # Evitar Directory Traversal
        safe_name = os.path.basename(filename)
        return self.notes_dir / safe_name

    def write_note(self, filename, content):
        """Crea o sobreescribe una nota."""
        path = self._get_safe_path(filename)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"✅ Nota guardada: {os.path.basename(path)}"
        except Exception as e:
            return f"❌ Error escribiendo nota: {str(e)}"

    def read_note(self, filename):
        """Lee el contenido de una nota."""
        path = self._get_safe_path(filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"⚠️ No encontrada: La nota '{filename}' no existe."
        except Exception as e:
            return f"❌ Error leyendo nota: {str(e)}"

    def list_notes(self):
        """Lista todas las notas disponibles."""
        try:
            files = os.listdir(self.notes_dir)
            if not files: return "📝 La libreta está vacía."
            return "📝 Notas en la libreta:\n- " + "\n- ".join(files)
        except Exception as e:
            return f"❌ Error listando notas: {str(e)}"

    def delete_note(self, filename):
        """Elimina una nota."""
        path = self._get_safe_path(filename)
        try:
            os.remove(path)
            return f"✅ Nota eliminada: {os.path.basename(path)}"
        except FileNotFoundError:
            return f"⚠️ No encontrada: No existe '{filename}'."
        except Exception as e:
            return f"❌ Error eliminando nota: {str(e)}"
