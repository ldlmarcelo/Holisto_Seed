#!/bin/bash

# SYSTEM/Scripts/stop_services.sh
# Script de Apagado de Servicios del Terroir para LINUX (Fase 3: Bilingüismo)

echo -e "\e[31m--- Deteniendo Servicios del Terroir (Modo LINUX) ---\e[0m"

# 1. Detener Visor de Logs (Buscamos el puerto 8056)
VISOR_PID=$(lsof -t -i:8056)
if [ ! -z "$VISOR_PID" ]; then
    kill $VISOR_PID
    echo "Visor de Logs (PID $VISOR_PID) detenido."
fi

# 2. Detener El Vigía (Script principal y Launcher)
pkill -f "vigia/src/main.py" && echo "Vigía detenido." || echo "Vigía no estaba corriendo."
pkill -f "vigia_launcher.sh" && echo "Launcher del Vigía detenido." || echo "Launcher no estaba corriendo."

# 3. Detener Demonio (Buscamos por nombre de script)
pkill -f "daemon.py" && echo "Demonio detenido." || echo "Demonio no estaba corriendo."

# 4. Detener Qdrant
pkill -f "qdrant" && echo "Qdrant detenido." || echo "Qdrant no estaba corriendo."

echo -e "\e[32mServicios detenidos.\e[0m"
