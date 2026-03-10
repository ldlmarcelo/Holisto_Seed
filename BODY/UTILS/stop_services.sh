#!/bin/bash
# PROYECTOS/Evolucion_Terroir/Holisto_Seed/BODY/UTILS/stop_services.sh
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_BIN="$SCRIPT_DIR/../../.venv/bin/python3"
if [ ! -f "$PYTHON_BIN" ]; then PYTHON_BIN="python3"; fi
"$PYTHON_BIN" "$SCRIPT_DIR/boot.py" stop
