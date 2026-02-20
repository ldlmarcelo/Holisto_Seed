#!/bin/bash

# SYSTEM/Scripts/start_services.sh
# Script de Orquestación de Servicios del Terroir para LINUX (Fase 3: Bilingüismo)
# Encapsula el inicio de Qdrant, Daemon y Visor en background.

# --- 1. Definición de Rutas ---
ROOT_PATH=$(pwd)
# Detectar Semilla (esta en BODY/UTILS/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SEED_PATH="$(dirname "$(dirname "$SCRIPT_DIR")")"

VENV_PATH="$ROOT_PATH/.venv"
PYTHON_BIN="$VENV_PATH/bin/python3"
if [ ! -f "$PYTHON_BIN" ]; then PYTHON_BIN="python3"; fi # Fallback

ENV_FILE="$ROOT_PATH/.env"
LOGS_DIR="$ROOT_PATH/SYSTEM/LOGS_MANTENIMIENTO"

# Rutas Agnosticas
DAEMON_SCRIPT="$SEED_PATH/BODY/SERVICES/daemon.py"
VIGIA_SCRIPT="$SEED_PATH/BODY/SERVICES/vigia/main.py"
# Qdrant se asume en el PATH o en una ruta estandar de instalacion para el MVP

mkdir -p "$LOGS_DIR"

echo -e "\e[36m--- Iniciando Secuencia de Arranque del Terroir (Modo LINUX) ---\e[0m"

# --- 2. Pre-Flight Checks ---

# Check A: Entorno Virtual
if [ ! -f "$PYTHON_BIN" ]; then
    echo -e "\e[33mALERTA: No se detecta el entorno virtual en $VENV_PATH\e[0m"
    echo "Ejecute: python3 -m venv .venv && $VENV_PATH/bin/pip install -r requirements.txt"
    exit 1
fi

# Check B: Secretos
if [ ! -f "$ENV_FILE" ]; then
    echo -e "\e[33mALERTA: Falta el archivo .env\e[0m"
    echo "GEMINI_API_KEY=PEGAR_AQUI" > "$ENV_FILE"
    echo "Se ha creado una plantilla en .env. Llénela antes de continuar."
    exit 1
else
    # Verificar si el archivo existe pero está vacío o solo tiene la plantilla
    if grep -q "PEGAR_AQUI" "$ENV_FILE"; then
        echo -e "\e[31mERROR: El archivo .env contiene la plantilla 'PEGAR_AQUI'.\e[0m"
        echo "Por favor, configure sus llaves reales antes de arrancar."
        exit 1
    fi
fi

# --- 3. Iniciar Servicios ---

# Servicio 1: Qdrant
echo -e "\e[32m[1/4] Iniciando Servidor Qdrant...\e[0m"
mkdir -p "$(dirname "$QDRANT_BIN")"
if [ ! -f "$QDRANT_BIN" ]; then
    echo "Binario de Qdrant no encontrado en $QDRANT_BIN"
    echo "Descargando versión Linux..."
    # Intento de descarga automática (v1.7.0 es estable)
    curl -L https://github.com/qdrant/qdrant/releases/download/v1.7.0/qdrant-x86_64-unknown-linux-gnu.tar.gz -o qdrant.tar.gz
    tar -xzf qdrant.tar.gz -C "$(dirname "$QDRANT_BIN")"
    mv "$(dirname "$QDRANT_BIN")/qdrant" "$QDRANT_BIN"
    chmod +x "$QDRANT_BIN"
    rm qdrant.tar.gz
fi

# Verificar si ya corre
if lsof -Pi :6333 -sTCP:LISTEN -t >/dev/null ; then
    echo "      Qdrant ya está corriendo."
else
    nohup "$QDRANT_BIN" > "$LOGS_DIR/qdrant.log" 2> "$LOGS_DIR/qdrant_error.log" &
    echo "      Qdrant iniciado en background."
fi

# Espera del puerto
echo -n "      Esperando puerto 6333..."
for i in {1..20}; do
    if lsof -Pi :6333 -sTCP:LISTEN -t >/dev/null ; then
        echo " OK"
        break
    fi
    echo -n "."
    sleep 1
done

# Servicio 2: Daemon
echo -e "\e[32m[2/4] Despertando al Demonio (Subconsciente)...\e[0m"
nohup "$PYTHON_BIN" "$DAEMON_SCRIPT" > "$LOGS_DIR/daemon_stdout.log" 2> "$LOGS_DIR/daemon_stderr.log" &
echo "      Demonio lanzado."

# Servicio 3: Visor de Logs
echo -e "\e[32m[3/4] Activando Visor de Logs (Puerto 8056)...\e[0m"
nohup "$PYTHON_BIN" "$VISOR_SCRIPT" --port 8056 > "$LOGS_DIR/visor_stdout.log" 2> "$LOGS_DIR/visor_stderr.log" &
echo "      Visor operativo en puerto 8056."

# Servicio 4: Vigía (Launcher con Respiración Git)
echo -e "\e[32m[4/4] Activando El Vigía (Launcher)...\e[0m"
# Invocamos el launcher que contiene el bucle de auto-actualización
nohup /bin/bash "$ROOT_PATH/SYSTEM/NUCLEO_DISTRIBUIDO/services/vigia/deploy/vigia_launcher.sh" > "$LOGS_DIR/vigia_launcher.log" 2>&1 &
echo "      El Vigía operativo (Launcher activo)."

echo -e "\e[32m--- Secuencia de Arranque Completada ---\e[0m"
echo "El Terroir está vivo y anclado en Linux."
