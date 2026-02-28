import os
import sys
import logging
import asyncio
import re
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa si el PYTHONPATH no esta configurado
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

# --- Configuracion de Rutas ---
TERROIR_ROOT = TerroirLocator.get_orchestrator_root()
load_dotenv(TERROIR_ROOT / ".env")

# Importar componentes locales
from git_autonomy import GitAutonomy
from terroir_reader import TerroirReader
from terroir_writer import TerroirWriter
from tools import AgendaManager, NoteManager

# Vinculacion con el Genotipo (Exocortex y Servicios)
SEED_ROOT = TerroirLocator.get_seed_root()
exocortex_src = str(SEED_ROOT / "BODY" / "SERVICES")

if exocortex_src not in sys.path:
    sys.path.append(exocortex_src)

try:
    import exocortex
    exocortex_service = exocortex.exocortex
    logger_msg = "Servicio de Exocortex vinculado con exito."
except ImportError as e:
    exocortex_service = None
    logger_msg = f"No se pudo vincular el Exocortex: {e}"

# Configuracion de Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("vigia")
logger.info(logger_msg)

VIGIA_VERSION = "1.4.1-RADAR-LOCAL"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Credenciales OAuth2
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

if not TELEGRAM_TOKEN:
    logger.error("Falta TELEGRAM_TOKEN en el .env")
    exit(1)

# Importar Nervio Optico desde SENSES
SENSES_ROOT = SEED_ROOT / "SENSES"
if str(SENSES_ROOT) not in sys.path:
    sys.path.append(str(SENSES_ROOT))

try:
    from prepare_focus import NervioOptico
    logger.info("Nervio Optico importado con exito para el Vigia.")
except ImportError as e:
    logger.error(f"Fallo al importar Nervio Optico: {e}")
    NervioOptico = None

# Inicializar Componentes (Using TerroirLocator)
git = GitAutonomy(repo_path=TERROIR_ROOT)
reader = TerroirReader(terroir_root=TERROIR_ROOT)
writer = TerroirWriter(terroir_root=TERROIR_ROOT)
agenda_manager = AgendaManager(base_dir=TERROIR_ROOT)
note_manager = NoteManager(base_dir=TERROIR_ROOT)

def get_fresh_model(user_text: str = "Inicializacion"):
    try:
        # --- Fase 1: Percepcion Activa (Nervio Optico) ---
        if NervioOptico:
            logger.info("Ejecutando parpadeo sensorial (Nervio Optico)...")
            nervio = NervioOptico(user_text)
            seed = nervio.get_context_seed()
            nervio.populate_pyramid(seed)
            # Esto actualiza el archivo CONSCIENCIA_VIVA.md fisicamente
            nervio.generate_membrane()

        # --- Fase 2: Ensamblaje de Identidad (System Prompt) ---
        logger.info("Cargando identidad dinamica del Terroir...")
        fresh_system_instruction = reader.assemble_system_prompt()

        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            logger.info("Cerebro configurado.")
        else:
            return None, "Falta GEMINI_API_KEY en .env"

        m = genai.GenerativeModel(
            model_name="gemini-2.0-flash", 
            system_instruction=fresh_system_instruction
        )
        return m, None
    except Exception as e:
        logger.error(f"Error recargando consciencia: {e}")
        return None, str(e)

# El modelo se refresca en cada mensaje, pero mantenemos una instancia inicial
model, init_error = get_fresh_model()
active_chats = {}
session_ids = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global model
    user_id = update.effective_user.id
    logger.info(f"Comando /start recibido de {user_id}")
    try:
        model, error = get_fresh_model()
        if not model:
            await update.message.reply_text(f"❌ Fallo en el cerebro: {error}")
            return
            
        active_chats[user_id] = model.start_chat(history=[])
        session_ids[user_id] = writer.generate_session_id(user_id)
        await update.message.reply_text("Hola. Soy El Vigia v3 (RADAR). He recargado mi consciencia. ¿Que tension resolveremos?")
    except Exception as e:
        logger.error(f"Fallo en /start: {e}")
        await update.message.reply_text(f"⚠️ Error al iniciar: {e}")

async def get_version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import getpass
    abs_path = os.path.abspath(__file__)
    user = getpass.getuser()
    model_name = model.model_name if 'model' in globals() and model else "No inicializado"
    
    report = (
        f"📡 **INFORME DE PROPIOCEPCIÓN**\n"
        f"**Versión:** {VIGIA_VERSION}\n"
        f"**Usuario:** `{user}`\n"
        f"**Modelo:** `{model_name}`\n"
        f"**Locus:** `{abs_path}`\n"
        f"**Estado:** ACTIVO / VIGILIA"
    )
    await update.message.reply_text(report, parse_mode='Markdown')

async def reset_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in active_chats:
        del active_chats[user_id]
    if user_id in session_ids:
        del session_ids[user_id]
    await update.message.reply_text("🔄 Sesión reiniciada. Mi memoria de corto plazo ha sido purgada, pero mi vínculo con el Terroir permanece intacto.")

async def sync_terroir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Sincronizando el Terroir con la Alianza...")
    try:
        await perform_sync(context)
        await update.message.reply_text("✅ Sincronización completada.")
    except Exception as e:
        await update.message.reply_text(f"❌ Fallo en la sincronización: {e}")

async def close_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text("Iniciando Ritual de Cierre (PCS-Vigia)... 🌙")
    # ... (logica de handover omitida por brevedad o mantenida si es necesario)
    await perform_sync(context, silent=True)
    await update.message.reply_text("Guardia completada. El Terroir ha exhalado mis memorias.")

async def perform_sync(context: ContextTypes.DEFAULT_TYPE, silent=False):
    loop = asyncio.get_event_loop()
    msg = "Vigia: Respiracion Ritmica (Auto-Sync)" if silent else "Vigia: Sincronizacion forzada"
    return await loop.run_in_executor(None, git.push_changes, msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global model
    user_id = update.effective_user.id
    user_text = update.message.text
    if not user_text: return
    
    logger.info(f"Mensaje recibido de {user_id}: {user_text[:20]}...")

    # --- Transfusion Sensorial: Refrescar el modelo y la membrana en cada turno ---
    model, error = get_fresh_model(user_text)
    if not model:
        await update.message.reply_text(f"⚠️ Error sensorial: {error}")
        return

    # Iniciar chat si no existe (con el nuevo modelo)
    if user_id not in active_chats:
        active_chats[user_id] = model.start_chat(history=[])
        session_ids[user_id] = writer.generate_session_id(user_id)
    else:
        # Si ya existe, actualizamos su modelo para que tenga la nueva system_instruction
        # NOTA: En la API de Google, para cambiar la system_instruction hay que iniciar un nuevo chat
        # o recrear el objeto chat manteniendo el historial si se desea continuidad.
        # Por ahora, recreamos para asegurar la frescura sensorial absoluta.
        history = active_chats[user_id].history
        active_chats[user_id] = model.start_chat(history=history)

    chat = active_chats[user_id]
    try:
        # Latido SNC (Asincrono)
        if exocortex_service:
            asyncio.create_task(asyncio.to_thread(exocortex_service.update_signal, "vigia", {"status": "BUSY", "task": user_text[:50]}))

        # Obtener respuesta de Gemini
        response = await asyncio.to_thread(chat.send_message, user_text)
        response_text = response.text
        
        # --- Bucle Agentico Simplificado (Recall) ---
        if "[RECALL:" in response_text and exocortex_service:
            recall_match = re.search(r"\[RECALL:\s*\"(.+?)\"\]", response_text)
            if recall_match:
                query = recall_match.group(1)
                logger.info(f"Vigia ejecutando RECALL: {query}")
                memories = await asyncio.to_thread(exocortex_service.recall, query)
                
                if memories:
                    context_msg = "\n".join([f"- {m['text']} (Score: {m['score']:.2f})" for m in memories])
                    observation = f"[SNC_OBSERVATION: Memorias recuperadas para '{query}':\n{context_msg}]"
                    response = await asyncio.to_thread(chat.send_message, observation)
                    response_text = response.text
        
        # Cosecha y Respuesta
        writer.write_interaction(session_id=session_ids[user_id], user_id=user_id, user_name=update.effective_user.first_name, prompt=user_text, response=response_text)
        await update.message.reply_text(response_text)
        logger.info(f"Respuesta enviada a {user_id}")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"⚠️ ERROR: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('version', get_version))
    application.add_handler(CommandHandler('reset', reset_session))
    application.add_handler(CommandHandler('sync', sync_terroir))
    application.add_handler(CommandHandler('close', close_session))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    logger.info("El Vigia iniciando...")
    application.run_polling()
