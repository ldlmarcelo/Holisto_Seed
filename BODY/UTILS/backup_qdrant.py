import os
import subprocess
import datetime
from pathlib import Path
import json
import sys

# --- Configuración del Locus ---
# El script asume que corre en el NUC donde Qdrant es un servicio de systemd
QDRANT_STORAGE_DIR = "/var/lib/qdrant/storage"  # Ruta estándar en Linux
BACKUP_TEMP_DIR = "/tmp/holisto_backups"
DRIVE_FOLDER_NAME = "Holisto_Backups_Semanticos"

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    return True

def backup():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"qdrant_backup_{timestamp}.tar.gz"
    local_backup_path = os.path.join(BACKUP_TEMP_DIR, backup_filename)
    
    Path(BACKUP_TEMP_DIR).mkdir(parents=True, exist_ok=True)
    
    print(f"--- Iniciando Backup Metabólico: {timestamp} ---")
    
    # 1. Parada de seguridad
    print("Deteniendo Qdrant...")
    run_command("sudo systemctl stop qdrant")
    
    # 2. Compresión
    print(f"Comprimiendo exocórtex en {local_backup_path}...")
    if run_command(f"tar -czf {local_backup_path} -C {QDRANT_STORAGE_DIR} ."):
        
        # 3. Reinicio inmediato para minimizar 'amnesia'
        print("Reiniciando Qdrant...")
        run_command("sudo systemctl start qdrant")
        
        # 4. Envío a Drive vía Skill
        print("Enviando a Google Drive...")
        # Nota: Aquí llamamos a la lógica de la skill google-drive
        # En el NUC, la skill estará instalada en el PATH o vía el Orquestador
        # Por ahora, dejamos el 'call' preparado para ser ejecutado por el orquestador
        
        print(f"Backup local completado: {local_backup_path}")
        print("Siguiente paso: Ejecutar skill 'google-drive' con comando 'upload_file'")
    else:
        print("Fallo en la compresión. Reiniciando servicios de emergencia.")
        run_command("sudo systemctl start qdrant")

if __name__ == "__main__":
    # Solo ejecutar si estamos en Linux (NUC)
    if sys.platform != "win32":
        backup()
    else:
        print("Aviso: El script de backup está diseñado para el entorno Linux del NUC.")
