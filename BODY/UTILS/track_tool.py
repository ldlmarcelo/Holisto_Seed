import sys
import subprocess
import os
from pathlib import Path

def main():
    # Puente hacia event_sensor.py
    current_dir = Path(__file__).resolve().parent
    script_path = current_dir / "event_sensor.py"
    
    # Mapeo de argumentos de track_tool a event_sensor
    new_args = [sys.executable, str(script_path), "--type", "usage"]
    new_args.extend(sys.argv[1:])
    
    subprocess.run(new_args)

if __name__ == "__main__":
    main()
