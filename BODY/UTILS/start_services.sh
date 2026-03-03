#!/bin/bash

# PROYECTOS/Evolucion_Terroir/Holisto_Seed/BODY/UTILS/start_services.sh
# Script de Orquestación de Servicios del Terroir para LINUX (v3 - Genotipo Seed)
# Encapsula el inicio del Daemon y el Vigía en background.

# --- 1. Definición de Rutas ---
# El Orquestador es la raíz (donde se ejecuta el script usualmente)
ROOT_PATH=$(pwd)
# Detectar Semilla (esta en BODY/UTILS/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SEED_PATH="$(dirname "$(dirname "$SCRIPT_DIR")")"

VENV_PATH="$ROOT_PATH/.venv"
PYTHON_BIN="$VENV_PATH/bin/python3"
if [ ! -f "$PYTHON_BIN" ]; then PYTHON_BIN="python3"; fi # Fallback

ENV_FILE="$ROOT_PATH/.env"
LOGS_DIR="$ROOT_PATH/SYSTEM/LOGS_MANTENIMIENTO"

# Rutas Agnosticas (dentro del Seed)
DAEMON_SCRIPT="$SEED_PATH/BODY/SERVICES/daemon.py"
VIGIA_SCRIPT="$SEED_PATH/BODY/SERVICES/vigia/main.py"

mkdir -p "$LOGS_DIR"

echo -e "\e[36m--- Iniciando Secuencia de Arranque del Terroir (Genotipo Seed) ---\e[0m"

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
    if grep -q "PEGAR_AQUI" "$ENV_FILE"; then
        echo -e "\e[31mERROR: El archivo .env contiene la plantilla 'PEGAR_AQUI'.\e[0m"
        echo "Por favor, configure sus llaves reales antes de arrancar."
        exit 1
    fi
fi

# --- 3. Iniciar Servicios ---

# Servicio 1: Subconsciente (Daemon)
echo -e "\e[32m[1/2] Despertando al Demonio (Subconsciente)...\e[0m"
nohup "$PYTHON_BIN" "$DAEMON_SCRIPT" > "$LOGS_DIR/daemon_stdout.log" 2> "$LOGS_DIR/daemon_stderr.log" &
echo "      Demonio lanzado."

# Servicio 2: Vigía (Telegram Bot)
echo -e "\e[32m[2/2] Activando El Vigía (Telegram Bot)...\e[0m"
# En Linux, corremos el main.py directamente por ahora (la respiración Git se gestiona externamente)
nohup "$PYTHON_BIN" "$VIGIA_SCRIPT" > "$LOGS_DIR/vigia_stdout.log" 2> "$LOGS_DIR/vigia_stderr.log" &
echo "      El Vigía operativo."

echo -e "\e[32m--- Secuencia de Arranque Completada ---\e[0m"
echo "El Terroir está vivo y anclado en el Genotipo."
