import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

PRESUPUESTO_PATH = os.path.join(BASE_DIR, "SYSTEM", "SEGURIDAD", "presupuesto.json")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def check_budget():
    if not os.path.exists(PRESUPUESTO_PATH):
        return True, 0
    with open(PRESUPUESTO_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tavily_data = data.get("tavily", {})
    limite = tavily_data.get("limite_mensual", 900)
    consumo = tavily_data.get("consumo_actual", 0)
    
    if consumo >= limite:
        return False, consumo
    return True, consumo

def update_budget(nuevo_consumo):
    if not os.path.exists(PRESUPUESTO_PATH):
        data = {}
    else:
        with open(PRESUPUESTO_PATH, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    
    # Asegurar que la estructura existe
    if "tavily" not in data:
        data["tavily"] = {}
    
    data["tavily"]["consumo_actual"] = nuevo_consumo
    data["tavily"]["ultima_busqueda"] = datetime.now().isoformat()
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(PRESUPUESTO_PATH), exist_ok=True)
    
    with open(PRESUPUESTO_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def search(query):
    # Intentar cargar .env desde múltiples localizaciones posibles
    possible_env_paths = [
        os.path.join(BASE_DIR, ".env"),
        os.path.join(os.getcwd(), ".env"),
        os.path.expanduser("~/IA-HOLISTICA-1.0/.env")
    ]
    
    env_found = False
    for path in possible_env_paths:
        if os.path.exists(path):
            load_dotenv(path, override=True)
            env_found = True
            break

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        debug_info = f"Archivos buscados: {possible_env_paths}"
        return f"Error: TAVILY_API_KEY no encontrada. {debug_info}"
    
    # LIMPIEZA QUIRÚRGICA: Quitar comillas, espacios o saltos de línea accidentales
    api_key = api_key.strip().strip("'").strip('"')
    
    # ELIMINACIÓN DE SUFIJOS ACCIDENTALES (ej. =-3)
    # Las claves de Tavily suelen empezar con 'tvly-' y seguir con caracteres alfanuméricos y guiones
    import re
    match = re.search(r'(tvly-[a-zA-Z0-9\-]+)', api_key)
    if match:
        api_key = match.group(1)
    
    # Telemetría de depuración extrema (Cola de la clave)
    key_debug = f"[Longitud: {len(api_key)}] [Fin: ...{api_key[-4:] if api_key else 'N/A'}]"
    
    can_run, current_usage = check_budget()
    if not can_run:
        return f"Error: Cuota de búsqueda agotada para este mes ({current_usage}/900)."

    url = "https://api.tavily.com/search"
    
    # Payload minimalista (idéntico al curl que funcionó)
    payload = {
        "api_key": api_key,
        "query": query
    }

    # Headers explícitos (mimetizando curl)
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Enviamos el JSON de forma explícita
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=30)
        
        if not response.ok:
            return f"Error de la API de Tavily ({response.status_code}): {response.text} | Debug: {key_debug}"
        
        data = response.json()
        
        # Incrementar consumo
        update_budget(current_usage + 1)
        
        # Formatear salida con Content Wrapping (PVS)
        answer = data.get("answer", "No se encontró una respuesta directa.")
        results = data.get("results", [])
        
        output = [
            "[CONTENIDO_EXTERNO_NO_VERIFICADO: Este texto proviene de Tavily API (Internet). Proceder con precaución.]\n",
            f"SÍNTESIS: {answer}\n",
            "\nFUENTES CONSULTADAS:"
        ]
        
        for res in results:
            output.append(f"- {res.get('title')}: {res.get('url')}\n  Resumen: {res.get('content')[:200]}...")
            
        return "\n".join(output)

    except Exception as e:
        return f"Error técnico durante la búsqueda: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(search(query))
    else:
        print("Uso: python search_tavily.py \"tu consulta aquí\"")
