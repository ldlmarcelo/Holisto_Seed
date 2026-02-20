import sys
import subprocess
import os

def main():
    # Puente hacia event_sensor.py manteniendo compatibilidad de argumentos
    # Argumentos esperados: --tool, --success, --time, --details
    script_path = os.path.join(os.path.dirname(__file__), "event_sensor.py")
    
    # Mapeo de argumentos de track_tool a event_sensor
    new_args = [sys.executable, script_path, "--type", "usage"]
    new_args.extend(sys.argv[1:])
    
    subprocess.run(new_args)

if __name__ == "__main__":
    main()
