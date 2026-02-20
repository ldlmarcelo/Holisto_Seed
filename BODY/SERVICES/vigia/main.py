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

# --- Configuracion de Rutas ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))
def find_terroir_root(start_dir):
    current = os.path.abspath(start_dir)
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, ".env")):
            return current
        current = os.path.dirname(current)
    return os.path.abspath(os.path.join(start_dir, "../../../../../.."))

BASE_DIR = find_terroir_root(current_script_dir)
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Importar componentes locales
from git_autonomy import GitAutonomy
from terroir_reader import TerroirReader
from terroir_writer import TerroirWriter
from tools import AgendaManager, NoteManager

# Vinculacion con el Genotipo (Exocortex y Scripts)
seed_root = os.path.join(BASE_DIR, "PROYECTOS", "Evolucion_Terroir", "Holisto_Seed")
exocortex_src = os.path.join(seed_root, "BODY", "SERVICES")
scripts_src = os.path.join(BASE_DIR, "SYSTEM", "Scripts")

for path in [exocortex_src, scripts_src]:
    if path not in sys.path:
        sys.path.append(path)

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

VIGIA_VERSION = "1.4.0-SEED (Unified Genotype Architecture)"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Credenciales OAuth2
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

if not TELEGRAM_TOKEN:
    logger.error("Falta TELEGRAM_TOKEN en el .env")
    exit(1)

# Inicializar Componentes
git = GitAutonomy(repo_path=BASE_DIR)
reader = TerroirReader(terroir_root=BASE_DIR)
writer = TerroirWriter(terroir_root=BASE_DIR)
agenda_manager = AgendaManager(base_dir=BASE_DIR)
note_manager = NoteManager(base_dir=BASE_DIR)

def get_fresh_model():
    try:
        logger.info("Cargando identidad del Terroir...")
        fresh_system_instruction = reader.assemble_system_prompt()

        if CLIENT_ID and CLIENT_SECRET and REFRESH_TOKEN:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            creds = Credentials(
                token=None, refresh_token=REFRESH_TOKEN,
                client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                token_uri="https://oauth2.googleapis.com/token"
            )
            creds.refresh(Request())
            genai.configure(credentials=creds)
        elif GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
        else:
            return None

        return genai.GenerativeModel(
            model_name="gemini-2.0-flash", # Actualizado a 2.0
            system_instruction=fresh_system_instruction
        )
    except Exception as e:
        logger.error(f"Error recargando consciencia: {e}")
        return None

model = get_fresh_model()
active_chats = {}
session_ids = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global model
    user_id = update.effective_user.id
    model = get_fresh_model()
    active_chats[user_id] = model.start_chat(history=[])
    session_ids[user_id] = writer.generate_session_id(user_id)
    await update.message.reply_text("Hola. Soy El Vigia. He recargado mi consciencia desde el Genotipo Seed. ¿Que tension resolveremos?")

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
    user_id = update.effective_user.id
    user_text = update.message.text
    if not user_text: return

    if user_id not in active_chats:
        active_chats[user_id] = model.start_chat(history=[])
        session_ids[user_id] = writer.generate_session_id(user_id)

    chat = active_chats[user_id]
    try:
        loop = asyncio.get_event_loop()
        # Latido SNC
        if exocortex_service:
            await loop.run_in_executor(None, exocortex_service.update_signal, "vigia", {"status": "BUSY", "task": user_text[:50]})

        response = await loop.run_in_executor(None, chat.send_message, user_text)
        response_text = response.text
        
        # Procesar herramientas [RECALL], [SEARCH], etc. (Simplificado para esta restauracion)
        # TODO: Re-implementar bucle agentico completo si es necesario
        
        writer.write_interaction(session_id=session_ids[user_id], user_id=user_id, user_name=update.effective_user.first_name, prompt=user_text, response=response_text)
        await update.message.reply_text(response_text)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"⚠️ ERROR: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    logger.info("El Vigia iniciando...")
    application.run_polling()
