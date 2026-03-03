#!/bin/bash

# PROYECTOS/Evolucion_Terroir/Holisto_Seed/BODY/UTILS/stop_services.sh
# Script de Detención de Servicios del Terroir (Modo LINUX)

echo "--- Deteniendo Servicios del Terroir (Modo LINUX) ---"

# 1. Detener el Vigía
VIGIA_PID=$(ps aux | grep 'vigia/main.py' | grep -v grep | awk '{print $2}')
if [ -n "$VIGIA_PID" ]; then
    echo "Deteniendo El Vigía (PID: $VIGIA_PID)..."
    kill $VIGIA_PID
else
    echo "El Vigía no estaba corriendo."
fi

# 2. Detener el Demonio
DAEMON_PID=$(ps aux | grep 'daemon.py' | grep -v grep | awk '{print $2}')
if [ -n "$DAEMON_PID" ]; then
    echo "Deteniendo Demonio (PID: $DAEMON_PID)..."
    kill $DAEMON_PID
else
    echo "El Demonio no estaba corriendo."
fi

echo "--- Servicios Detenidos ---"
