import json
import os
import argparse
from datetime import datetime, timezone

# Rutas de logs
USAGE_LOG = "SYSTEM/LOGS_MANTENIMIENTO/herramientas.jsonl"
FRICTION_LOG = "SYSTEM/LOGS_MANTENIMIENTO/fricciones_ejecucion.jsonl"

def log_event(event_type, tool, success, session_id=None, error_pattern=None, details=None, execution_time=None):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type, # usage, friction, anomaly
        "tool": tool,
        "success": success,
        "session_id": session_id or "unknown",
        "error_pattern": error_pattern,
        "execution_time_sec": execution_time,
        "details": details
    }
    
    # Determinar el archivo de destino
    log_file = FRICTION_LOG if event_type == "friction" else USAGE_LOG
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sensor de Eventos Operativos del Terroir.")
    parser.add_argument("--type", choices=["usage", "friction", "anomaly"], default="usage", help="Tipo de evento")
    parser.add_argument("--tool", required=True, help="Nombre de la herramienta")
    parser.add_argument("--success", choices=["true", "false"], required=True, help="Resultado")
    parser.add_argument("--session", help="ID de la sesión")
    parser.add_argument("--pattern", help="Patrón de error (para fricciones)")
    parser.add_argument("--details", help="Detalles adicionales")
    parser.add_argument("--time", type=float, help="Tiempo de ejecución")
    
    args = parser.parse_args()
    
    is_success = args.success.lower() == "true"
    
    log_event(
        event_type=args.type,
        tool=args.tool,
        success=is_success,
        session_id=args.session,
        error_pattern=args.pattern,
        details=args.details,
        execution_time=args.time
    )
