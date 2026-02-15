import os
import json
import uuid
from datetime import datetime, timezone, timedelta

class AgendaManager:
    def __init__(self, storage_path=None):
        """
        Inicia el gestor de agenda con una ruta de almacenamiento.
        Prioriza variables de entorno para portabilidad (Asepsia).
        """
        self.storage_path = storage_path or os.getenv("HOLISTO_AGENDA_FILE")
        if not self.storage_path:
            # Fallback relativo a la raiz del proyecto si no hay env
            self.storage_path = "SYSTEM/AGENDA/recordatorios.json"

    def _load(self):
        if not os.path.exists(self.storage_path):
            return []
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def _save(self, data):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_reminder(self, title, description, target_date, target_time="00:00", priority="low"):
        agenda = self._load()
        new_item = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "target_date": target_date,
            "target_time": target_time,
            "priority": priority,
            "status": "pendiente",
            "created_at": datetime.now().isoformat()
        }
        agenda.append(new_item)
        self._save(agenda)
        return new_item

    def check_deadlines(self, user_offset=-3):
        """
        Escanea la agenda y devuelve los items que deben ser notificados.
        """
        agenda = self._load()
        now_user = datetime.now(timezone.utc) + timedelta(hours=user_offset)
        now_comparison = now_user.replace(tzinfo=None)

        to_notify = []
        updated = False

        for item in agenda:
            if item['status'] != 'pendiente':
                continue

            target_dt_str = f"{item['target_date']} {item.get('target_time', '00:00')}"
            try:
                target_dt = datetime.strptime(target_dt_str, "%Y-%m-%d %H:%M")
            except ValueError:
                target_dt = datetime.strptime(item['target_date'], "%Y-%m-%d")

            if now_comparison >= target_dt:
                item['status'] = 'notificado'
                item['last_triggered'] = now_comparison.isoformat()
                to_notify.append(item)
                updated = True

        if updated:
            self._save(agenda)
        
        return to_notify

    def update_status(self, item_id, new_status):
        agenda = self._load()
        updated = False
        for item in agenda:
            if item['id'] == item_id:
                item['status'] = new_status
                updated = True
                break
        if updated:
            self._save(agenda)
        return updated

if __name__ == "__main__":
    # Prueba rapida de funcionamiento
    manager = AgendaManager("test_agenda.json")
    print("Agregando recordatorio de prueba...")
    manager.add_reminder("Prueba", "Esta es una prueba de la Skill modular", "2026-02-15")
    pending = manager.check_deadlines()
    print(f"Items a notificar: {len(pending)}")
    if os.path.exists("test_agenda.json"):
        os.remove("test_agenda.json")
