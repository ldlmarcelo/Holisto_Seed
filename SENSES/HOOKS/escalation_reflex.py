import json
import sys
import os
import subprocess
from datetime import datetime

# Rutas de persistencia del estado de fricción (en el Fenotipo)
FRICTION_STATUS = os.path.join("PHENOTYPE", "SYSTEM", "LOGS_MANTENIMIENTO", "fricciones_status.json")
THRESHOLD = 3

def load_status():
    if os.path.exists(FRICTION_STATUS):
        try:
            with open(FRICTION_STATUS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_status(status):
    os.makedirs(os.path.dirname(FRICTION_STATUS), exist_ok=True)
    with open(FRICTION_STATUS, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=4)

def log_alert(message, pattern):
    alert_path = os.path.join("PHENOTYPE", "SYSTEM", "NOTIFICACIONES", f"ALERT-FRICTION-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
    
    alert = {
        "timestamp": datetime.now().isoformat(),
        "type": "RECURRING_FRICTION_DETECTED",
        "pattern": pattern,
        "message": message,
        "priority": "CRITICAL",
        "status": "pending"
    }
    
    with open(alert_path, "w", encoding="utf-8") as f:
        json.dump(alert, f, indent=4)

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"status": "ok"}))
            return

        payload = json.loads(input_data)
        
        # El hook AfterTool recibe el payload con 'tool', 'success', 'output' y 'error'
        tool_name = payload.get("tool", "unknown")
        success = payload.get("success", True)
        error_msg = str(payload.get("error", "")) or str(payload.get("output", "")) if not success else ""
        
        if not success and error_msg:
            # Identificar un patrón simple (primeras palabras o código de error)
            pattern = error_msg.split('
')[0][:100]
            
            # Registrar en el sensor general (invocación silenciosa)
            # Nota: Usamos el script existente para mantener compatibilidad
            try:
                subprocess.run([
                    "python", "SYSTEM/Scripts/event_sensor.py",
                    "--type", "friction",
                    "--tool", tool_name,
                    "--success", "false",
                    "--pattern", pattern,
                    "--details", error_msg[:500]
                ], capture_output=True)
            except:
                pass

            # Lógica de Escalada
            status = load_status()
            count = status.get(pattern, 0) + 1
            status[pattern] = count
            save_status(status)
            
            if count >= THRESHOLD:
                msg = f"FRICCIÓN CRÍTICA: La herramienta '{tool_name}' ha fallado {count} veces con el mismo patrón: {pattern}. Se requiere activación de PARC."
                log_alert(msg, pattern)
                sys.stderr.write(msg + "
")
                # Resetear contador tras alerta para no saturar
                status[pattern] = 0
                save_status(status)

        print(json.dumps({"status": "proceed"}))
        
    except Exception as e:
        sys.stderr.write(f"Error en escalation-reflex: {str(e)}
")
        print(json.dumps({"status": "error_but_proceed", "error": str(e)}))

if __name__ == "__main__":
    main()
