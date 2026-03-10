import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

# Cargar las variables que pegaste
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: No encontre CLIENT_ID o CLIENT_SECRET en el archivo .env")
    exit(1)

# Scopes para Gemini API
SCOPES = ['https://www.googleapis.com/auth/generative-language.retriever']

print("Iniciando ritual de autorizacion OAuth2...")
print("Se abrira tu navegador. Por favor, autoriza la aplicacion.")

try:
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        SCOPES
    )

    # Lanza el servidor local para recibir el callback
    creds = flow.run_local_server(port=0)

    token = creds.refresh_token
    print("\nAUTORIZACION EXITOSA")
    print("REFRESH_TOKEN obtenido correctamente.")
    
    # Auto-guardado en .env
    env_path = ".env"
    with open(env_path, "r") as f:
        lines = f.readlines()
    
    new_lines = []
    found = False
    for line in lines:
        if line.startswith("REFRESH_TOKEN="):
            new_lines.append(f"REFRESH_TOKEN={token}\n")
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        new_lines.append(f"REFRESH_TOKEN={token}\n")
            
    with open(env_path, "w") as f:
        f.writelines(new_lines)
        
    print("REFRESH_TOKEN guardado en .env satisfactoriamente.")

except Exception as e:
    print(f"ERROR durante el flujo: {e}")
