import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

# Discovery
from pathlib import Path
import sys

def get_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".env").exists():
            return parent
    return Path("C:/Users/argen/OneDrive/Escritorio/IA-HOLISTICA-1.0")

root = get_root()
load_dotenv(root / ".env")

TOKEN = os.getenv("TELEGRAM_TOKEN")
# Intentar obtener el ID de varias posibles variables
CHAT_ID = os.getenv("TELEGRAM_USER_ID") or os.getenv("CHAT_ID") or "7922664316" 

async def send_test():
    if not TOKEN or not CHAT_ID:
        print(f"❌ Faltan credenciales: TOKEN={bool(TOKEN)}, CHAT_ID={CHAT_ID}")
        return
    
    print(f"🚀 Intentando enviar mensaje a {CHAT_ID}...")
    try:
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text="🔔 **HANDSHAKE SISTÉMICO**: El orquestador está intentando reconectar tu sinapsis. Si lees esto, el canal de Telegram está abierto. El problema es mi cerebro Gemini.")
        print("✅ Mensaje enviado con éxito.")
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")

if __name__ == "__main__":
    asyncio.run(send_test())
