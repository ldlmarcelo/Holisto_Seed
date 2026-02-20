import json
import sys
import os
from datetime import datetime

# Configuración
USAGE_LOG = os.path.join("SYSTEM", "LOGS_MANTENIMIENTO", "herramientas.jsonl")
THRESHOLD = 2 # Máximo de acciones técnicas antes de exigir pausa
TECHNICAL_TOOLS = ["write_file", "replace", "run_shell_command"]

def main():
    try:
        # El hook recibe el contexto actual por stdin
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"status": "proceed"}))
            return

        payload = json.loads(input_data)
        session_id = payload.get("session_id")
        
        if not os.path.exists(USAGE_LOG):
            print(json.dumps({"status": "proceed"}))
            return

        technical_count = 0
        with open(USAGE_LOG, "r", encoding="utf-8") as f:
            # Leer de atrás hacia adelante para contar las últimas herramientas de ESTA sesión
            lines = f.readlines()
            for line in reversed(lines):
                try:
                    entry = json.loads(line)
                    # Si el log es del formato hook (con 'payload')
                    if entry.get("event") == "tool_execution":
                        data = entry.get("payload", {})
                        if data.get("session_id") != session_id:
                            break # Fin de los logs de esta sesión
                        
                        tool_name = data.get("tool_name")
                        if tool_name in TECHNICAL_TOOLS:
                            technical_count += 1
                    # Si el log es del formato legacy (event_sensor)
                    elif entry.get("session_id") == session_id:
                        if entry.get("tool") in TECHNICAL_TOOLS:
                            technical_count += 1
                except:
                    continue

        output = {"status": "proceed"}
        
        if technical_count >= THRESHOLD:
            msg = f"MANDATO PEG: Llevas {technical_count} acciones técnicas en esta sesión sin una pausa de validación. Debes detenerte y presentar evidencia (Anatomía UI, Flujos o URL) antes de continuar."
            output["systemMessage"] = f"[\033[93m! DELIVERY DISCIPLINE\033[0m] {msg}"
            output["hookSpecificOutput"] = {
                "additionalContext": f"ALERTA DE ABSORCIÓN (PEG): Has realizado {technical_count} cambios técnicos seguidos. El Protocolo de Entrega Granular te prohíbe seguir avanzando. ACCIÓN REQUERIDA: Presenta evidencia del trabajo actual y solicita feedback de Marcelo."
            }
        
        print(json.dumps(output))

    except Exception as e:
        sys.stderr.write(f"Error en delivery-discipline hook: {str(e)}
")
        print(json.dumps({"status": "error_but_proceed", "error": str(e)}))

if __name__ == "__main__":
    main()
