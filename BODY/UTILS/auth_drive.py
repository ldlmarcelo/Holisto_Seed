import os
import sys
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv, set_key

# --- Universal Root Discovery ---
def find_terroir_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        # Buscamos la raíz que contiene el .git principal o el requirements.txt del Terroir
        if (parent / ".git").exists() and (parent / "README.md").exists() and not (parent / "..").samefile(parent):
             if "Holisto_Seed" not in parent.name: # Evitar entrar en la raíz del submódulo
                return parent
    # Fallback al primer ancestro con .git
    for parent in current.parents:
        if (parent / ".git").exists():
            return parent
    return Path.cwd()

terroir_root = find_terroir_root()
env_path = terroir_root / ".env"
load_dotenv(env_path)

def get_env_var(var_name):
    """Lee una variable directamente del archivo .env para evitar cache de entorno."""
    with open(env_path, "r") as f:
        for line in f:
            if line.startswith(f"{var_name}="):
                return line.split("=")[1].strip()
    return None

def main():
    client_id = get_env_var("CLIENT_ID")
    client_secret = get_env_var("CLIENT_SECRET")
    
    print(f"DEBUG: Usando CLIENT_ID (leído directamente) = {client_id}")
    
    if not client_id or not client_secret or "TU_CLIENT_ID" in client_id:
        print("❌ Error: Credenciales no válidas en el .env")
        return

    # Configuración del cliente para el flujo USANDO LAS VARIABLES DEL .ENV
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    }

    # Definir los alcances (scopes) para acceso total a Drive
    scopes = ["https://www.googleapis.com/auth/drive"]

    flow = InstalledAppFlow.from_client_config(client_config, scopes=scopes)

    # Intentar flujo local
    try:
        print("\n🔑 --- INICIANDO AUTORIZACIÓN DE GOOGLE DRIVE ---")
        print("Se abrirá una ventana en tu navegador.")
        print("Por favor, selecciona la cuenta: marceloiaholisto@gmail.com")
        
        # Uso run_local_server para mayor comodidad del usuario
        creds = flow.run_local_server(port=0)
        
        refresh_token = creds.refresh_token
        
        if refresh_token:
            # Actualizar el .env usando set_key para no borrar otros comentarios
            set_key(str(env_path), "REFRESH_TOKEN", refresh_token)
            print("\n✅ ÉXITO: REFRESH_TOKEN actualizado en el .env")
            print(f"Cuenta vinculada con éxito.")
        else:
            print("\n⚠️ Advertencia: No se recibió un Refresh Token. Es posible que ya tuvieras acceso.")
            
    except Exception as e:
        print(f"\n❌ Error durante el proceso: {e}")

if __name__ == "__main__":
    main()
