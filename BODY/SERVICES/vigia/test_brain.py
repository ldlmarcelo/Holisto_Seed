import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Discovery
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

TERROIR_ROOT = TerroirLocator.get_orchestrator_root()
load_dotenv(TERROIR_ROOT / ".env")

print(f"TERROIR_ROOT: {TERROIR_ROOT}")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ ERROR: GEMINI_API_KEY no encontrada en el .env")
else:
    print(f"✅ GEMINI_API_KEY encontrada: {GEMINI_API_KEY[:5]}***")

try:
    from terroir_reader import TerroirReader
    reader = TerroirReader(terroir_root=TERROIR_ROOT)
    print("✅ TerroirReader cargado.")
    prompt = reader.assemble_system_prompt()
    print(f"✅ System Prompt ensamblado (Largo: {len(prompt)} chars)")
    
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name="gemini-3-flash-preview", system_instruction=prompt)
    print("✅ Modelo Generativo inicializado (v3).")
    
    chat = model.start_chat(history=[])
    print("🚀 Intentando mensaje de prueba: 'hola'...")
    response = chat.send_message("hola")
    print(f"📡 Respuesta del modelo: {response.text}")
    
except Exception as e:
    print(f"❌ FALLO EN LA PRUEBA: {str(e)}")
    import traceback
    traceback.print_exc()
