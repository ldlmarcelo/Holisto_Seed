import json
import sys
import os
from datetime import datetime

def log_event(event_type, data):
    log_path = os.path.join("SYSTEM", "LOGS_MANTENIMIENTO", "herramientas.jsonl")
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "payload": data
    }
    
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        sys.stderr.write(f"Error en Hook de Trazabilidad: {str(e)}\n")

def main():
    # El CLI pasa la información por stdin
    try:
        input_data = sys.stdin.read()
        if not input_data:
            # Si no hay input, al menos registramos que el hook fue invocado
            log_event("hook_triggered", {"status": "no_input"})
            print(json.dumps({"status": "ok"}))
            return

        payload = json.loads(input_data)
        log_event("tool_execution", payload)
        
        # El hook DEBE devolver un JSON válido a stdout
        print(json.dumps({"status": "proceed", "message": "Trazabilidad registrada."}))
        
    except Exception as e:
        sys.stderr.write(f"Fallo crítico en Hook: {str(e)}\n")
        # Devolvemos éxito para no bloquear la ejecución del agente por un error de log
        print(json.dumps({"status": "error_but_proceed", "error": str(e)}))

if __name__ == "__main__":
    main()
