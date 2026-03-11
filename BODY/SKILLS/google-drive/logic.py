import os
import sys
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# --- Universal Root Discovery ---
current_path = Path(__file__).resolve()
terroir_root = None
for parent in current_path.parents:
    if (parent / ".git").exists() or (parent / "requirements.txt").exists():
        terroir_root = parent
        break

if terroir_root:
    load_dotenv(terroir_root / ".env")
else:
    load_dotenv()

# --- Autenticación Resiliente ---
def get_drive_service():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    refresh_token = os.getenv("REFRESH_TOKEN")
    
    if not all([client_id, client_secret, refresh_token]):
        raise Exception("Faltan credenciales de Google (CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN) en el .env")
        
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    
    # Forzar el refresco del token de acceso inicial
    try:
        creds.refresh(Request())
    except Exception as e:
        # Si falla aquí, el problema es definitivamente la incompatibilidad Client/Token
        # Imprimimos más detalles para el diagnóstico
        error_msg = str(e)
        if "unauthorized_client" in error_msg:
            error_msg += " (Probable error en CLIENT_ID o CLIENT_SECRET)"
        raise Exception(f"Fallo al refrescar el token: {error_msg}")
        
    return build('drive', 'v3', credentials=creds)

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return
            
        payload = json.loads(input_data)
        command = payload.get("command")
        args = payload.get("arguments", {})
        
        service = get_drive_service()
        
        if command == "list_files":
            folder_id = args.get("folder_id", "root")
            results = service.files().list(
                q=f"'{folder_id}' in parents and trashed = false",
                pageSize=20, fields="files(id, name, mimeType, createdTime, modifiedTime)"
            ).execute()
            print(json.dumps({"status": "success", "files": results.get('files', [])}, indent=2))
            
        elif command == "search_files":
            query = args.get("query", "")
            results = service.files().list(
                q=f"name contains '{query}' and trashed = false",
                pageSize=20, fields="files(id, name, mimeType, createdTime, modifiedTime)"
            ).execute()
            print(json.dumps({"status": "success", "files": results.get('files', [])}, indent=2))
            
        elif command == "read_file":
            file_id = args.get("file_id")
            file_meta = service.files().get(fileId=file_id, fields="name, mimeType").execute()
            
            if file_meta['mimeType'] == 'application/vnd.google-apps.document':
                content = service.files().export(fileId=file_id, mimeType='text/plain').execute()
                text = content.decode('utf-8')
            else:
                content = service.files().get_media(fileId=file_id).execute()
                text = content.decode('utf-8')
                
            print(json.dumps({"status": "success", "name": file_meta['name'], "content": text}))
            
        elif command == "upload_file":
            local_path = args.get("local_path")
            folder_id = args.get("folder_id")
            
            file_metadata = {'name': os.path.basename(local_path)}
            if folder_id:
                file_metadata['parents'] = [folder_id]
                
            media = MediaFileUpload(local_path, resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(json.dumps({"status": "success", "file_id": file.get('id')}))
            
        else:
            print(json.dumps({"status": "error", "message": f"Comando desconocido: {command}"}))
            
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()
