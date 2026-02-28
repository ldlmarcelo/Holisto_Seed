import os
import sys
import time
import logging
import random
import json
import uuid
from datetime import datetime, timezone, timedelta
import asyncio
from telegram import Bot
from dotenv import load_dotenv

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa si el PYTHONPATH no esta configurado
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

# --- Configuracion de Rutas ---
TERROIR_ROOT = TerroirLocator.get_orchestrator_root()
load_dotenv(TERROIR_ROOT / ".env")

# Rutas del Fenotipo (Memoria Viva)
PHENOTYPE_ROOT = TerroirLocator.get_phenotype_root()
AGENDA_FILE = PHENOTYPE_ROOT / "SYSTEM" / "AGENDA" / "recordatorios.json"
CHAOS_HISTORY_FILE = TerroirLocator.get_mem_root() / "historial_de_caos.txt"
NOTIFICATIONS_DIR = PHENOTYPE_ROOT / "SYSTEM" / "NOTIFICACIONES"

# Rutas del Orquestador (Logs y Mantenimiento)
MAINTENANCE_LOGS_DIR = TerroirLocator.get_logs_dir()
os.makedirs(MAINTENANCE_LOGS_DIR, exist_ok=True)
DAEMON_LOG_FILE = MAINTENANCE_LOGS_DIR / "daemon.log"
FRICTION_LOG_FILE = MAINTENANCE_LOGS_DIR / "fricciones_ejecucion.jsonl"
FRICTION_STATUS_FILE = MAINTENANCE_LOGS_DIR / "fricciones_status.json"

# --- Configuracion de APIs ---
TELEGRAM_ENABLED = False
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_USER_ID") or os.getenv("CHAT_ID")
try:
    USER_OFFSET = int(os.getenv("USER_TIMEZONE_OFFSET", -3))
except:
    USER_OFFSET = -3

if TELEGRAM_TOKEN and CHAT_ID:
    TELEGRAM_ENABLED = True

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [DAEMON] - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(DAEMON_LOG_FILE, encoding='utf-8'), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("daemon")

# Import Exocortex Service from local package
try:
    import exocortex
    exocortex_service = exocortex.exocortex
except ImportError:
    from BODY.SERVICES import exocortex
    exocortex_service = exocortex.exocortex

# Integracion de Skills del Seed
SEED_ROOT = TerroirLocator.get_seed_root()
SKILLS_DIR = SEED_ROOT / "BODY" / "SKILLS"
AGENDA_SKILL_PATH = SKILLS_DIR / "agenda-management"
if AGENDA_SKILL_PATH not in sys.path: sys.path.append(AGENDA_SKILL_PATH)

try:
    # Intenta importar el modulo logic desde el path de la skill
    # Necesitamos asegurar que el script de la skill sea importable
    import importlib.util
    spec = importlib.util.spec_from_file_location("agenda_logic", os.path.join(AGENDA_SKILL_PATH, "scripts", "logic.py"))
    agenda_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agenda_mod)
    agenda_manager = agenda_mod.AgendaManager(AGENDA_FILE)
except Exception as e:
    logger.error(f"No se pudo cargar la Skill agenda-management del Seed: {e}")
    agenda_manager = None

# --- Heartbeat Settings ---
HEARTBEAT_INTERVAL = 300 # 5 min default

async def send_push(message):
    """Funcion asincrona para envio real."""
    if not TELEGRAM_ENABLED: return
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown', disable_notification=False)
        logger.info("Push Telegram EXITOSO.")
    except Exception as e:
        logger.error(f"Fallo Push Telegram: {e}")

def check_agenda():
    if not agenda_manager: return
    try:
        to_notify = agenda_manager.check_deadlines(user_offset=USER_OFFSET)

        for item in to_notify:
            # Sincronizar con el SNC
            try: exocortex_service.upsert_state(category="agenda", data=item)
            except Exception as e: logger.warning(f"Fallo sincronizacion PSN para agenda: {e}")

            # Notificacion fisica (SENSES)
            msg = f"🔔 *RECORDATORIO:* {item['title']}

{item['description']}"
            logger.info(f"Disparando recordatorio modular: {item['id']}")
            try:
                # Correr async en un thread o loop existente
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(send_push(msg))
                else:
                    asyncio.run(send_push(msg))
            except Exception as e:
                logger.error(f"Error enviando notificacion: {e}")

    except Exception as e:
        logger.error(f"Error en check_agenda (modular): {e}")

def check_frictions():
    """Analiza patrones de error recurrentes y escala si superan el umbral (PEF)."""
    if not os.path.exists(FRICTION_LOG_FILE): return

    counts = {}
    try:
        with open(FRICTION_LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                try:
                    event = json.loads(line)
                    pattern = event.get('error_pattern')
                    if pattern:
                        counts[pattern] = counts.get(pattern, 0) + 1
                except: continue

        status = {}
        if os.path.exists(FRICTION_STATUS_FILE):
            with open(FRICTION_STATUS_FILE, 'r', encoding='utf-8') as f:
                status = json.load(f)

        updated_status = False
        for pattern, count in counts.items():
            last_alert_count = status.get(pattern, 0)
            if count >= 3 and count > last_alert_count:
                notif_id = f"NOTIF-PEF-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                msg = f"⚠️ *ESCALADA DE FRICCION (PEF):* El patron '{pattern}' ha ocurrido {count} veces.

Es imperativo formalizar este aprendizaje en un Nodo de Conocimiento procedural."
                logger.info(f"Escalando friccion: {pattern} ({count} veces)")
                
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running(): loop.create_task(send_push(msg))
                    else: asyncio.run(send_push(msg))
                except: pass

                notif = {
                    "id": notif_id,
                    "type": "pef",
                    "priority": "alta",
                    "title": "Alerta de Friccion Recurrente",
                    "content": msg,
                    "timestamp": datetime.now().isoformat(),
                    "status": "no-leido"
                }
                notif_path = os.path.join(NOTIFICATIONS_DIR, f"{notif_id}.json")
                os.makedirs(NOTIFICATIONS_DIR, exist_ok=True)
                with open(notif_path, 'w', encoding='utf-8') as f:
                    json.dump(notif, f, indent=2, ensure_ascii=False)

                exocortex_service.upsert_state(category="notificacion", data=notif)
                status[pattern] = count
                updated_status = True

        if updated_status:
            with open(FRICTION_STATUS_FILE, 'w', encoding='utf-8') as f:
                json.dump(status, f, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Error en check_frictions: {e}")

def main_loop():
    logger.info("=== Demonio del Terroir Iniciado (Genotipo Seed) ===")

    while True:
        try:
            # 1. Verificar Agenda
            check_agenda()

            # 2. Verificar Fricciones (PEF)
            check_frictions()

            # 3. Latido del SNC
            if exocortex_service:
                exocortex_service.update_signal(node_id="daemon", data={"status": "active", "mode": "frugal"})

            time.sleep(HEARTBEAT_INTERVAL)
        except KeyboardInterrupt:
            logger.info("Demonio detenido por el usuario.")
            break
        except Exception as e:
            logger.error(f"Error en bucle principal: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main_loop()
