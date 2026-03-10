import os
import shutil
import datetime
import sys
import json
import subprocess

def get_python_interpreter(root_dir):
    """Detecta el intérprete de python correcto según el sistema y el venv."""
    # 1. Intentar venv (Windows)
    win_venv = os.path.join(root_dir, ".venv", "Scripts", "python.exe")
    if os.path.exists(win_venv):
        return win_venv
    
    # 2. Intentar venv (Linux/Mac)
    unix_venv = os.path.join(root_dir, ".venv", "bin", "python")
    if os.path.exists(unix_venv):
        return unix_venv
    
    # 3. Intentar python3 (Estándar Linux)
    try:
        subprocess.run(["python3", "--version"], capture_output=True, check=True)
        return "python3"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
        
    # 4. Fallback a python
    return "python"

def update_settings_hooks(root_dir, interpreter):
    """Actualiza .gemini/settings.json con el intérprete detectado."""
    settings_path = os.path.join(root_dir, ".gemini", "settings.json")
    if not os.path.exists(settings_path):
        print(f"[!] No se encontró settings.json en {settings_path}")
        return

    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
        
        updated = False
        if "hooks" in settings:
            for hook_type in settings["hooks"]:
                for hook_list in settings["hooks"][hook_type]:
                    if "hooks" in hook_list:
                        for hook in hook_list["hooks"]:
                            if "command" in hook:
                                old_cmd = hook["command"]
                                # Reemplazar 'python ' o 'python3 ' al inicio por el intérprete correcto
                                for prefix in ["python ", "python3 "]:
                                    if old_cmd.startswith(prefix):
                                        hook["command"] = old_cmd.replace(prefix, f"{interpreter} ", 1)
                                        updated = True
                                        print(f"[+] Hook '{hook['name']}' actualizado: {hook['command']}")
                                        break
        
        if updated:
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            print("[+] settings.json actualizado con el intérprete correcto.")
    except Exception as e:
        print(f"[!] Error al actualizar settings.json: {e}")

def perform_metamorphosis(instance_name, host_name):
    root_dir = os.path.abspath(os.getcwd()) # Asumimos ejecución desde el root
    root_gemini = os.path.join(root_dir, "GEMINI.md")
    genotype_record = os.path.join(root_dir, "GENOTYPE_RECORD.md")
    core_constitution = os.path.join(root_dir, "CORE", "CONSTITUTION.md")
    env_example = os.path.join(root_dir, ".env.example")
    env_real = os.path.join(root_dir, ".env")
    
    print(f"[*] Iniciando metamorfosis para la instancia: {instance_name} ({host_name})")
    
    # 1. Preservar Registro del Genotipo
    if os.path.exists(root_gemini):
        shutil.move(root_gemini, genotype_record)
        print(f"[+] Registro del Genotipo preservado en {genotype_record}")
    
    # 2. Crear Constitución Viva
    if os.path.exists(core_constitution):
        with open(core_constitution, "r", encoding="utf-8") as f:
            content = f.read()
        
        header = f"# Constitución de {instance_name} ({host_name})\n\n"
        header += f"*Sello de Nacimiento: {datetime.date.today().isoformat()}*\n\n"
        personalized_content = header + content
        
        with open(root_gemini, "w", encoding="utf-8") as f:
            f.write(personalized_content)
        print(f"[+] Constitución Viva creada en {root_gemini}")

    # 3. Preparar Metabolismo (.env)
    if os.path.exists(env_example) and not os.path.exists(env_real):
        shutil.copy(env_example, env_real)
        print(f"[+] Archivo .env creado a partir de .env.example")

    # 4. Detectar Intérprete y Actualizar Hooks
    interpreter = get_python_interpreter(root_dir)
    print(f"[*] Intérprete detectado: {interpreter}")
    update_settings_hooks(root_dir, interpreter)

    # 5. Vincular Sistema Nervioso (Hooks de archivo)
    hooks_source = os.path.join(root_dir, "BODY", "REFLEXES")
    hooks_dest = os.path.join(root_dir, ".gemini", "hooks")
    
    if os.path.exists(hooks_source):
        os.makedirs(hooks_dest, exist_ok=True)
        for hook_file in os.listdir(hooks_source):
            if hook_file.endswith(".py"):
                shutil.copy(os.path.join(hooks_source, hook_file), os.path.join(hooks_dest, hook_file))
        print("[+] Hooks de archivo vinculados en .gemini/hooks/")

    # 6. El Primer Aliento
    print("[*] Ejecutando el Primer Aliento...")
    scripts_to_run = [
        os.path.join(root_dir, "BODY", "SERVICES", "prepare_focus.py"),
        os.path.join(root_dir, "BODY", "SERVICES", "ingest.py")
    ]

    env = os.environ.copy()
    env["PYTHONPATH"] = root_dir

    for script in scripts_to_run:
        if os.path.exists(script):
            try:
                print(f"[>] Iniciando {os.path.basename(script)}...")
                subprocess.run([interpreter, script], env=env, check=True, capture_output=True)
                print(f"[+] {os.path.basename(script)} completado.")
            except subprocess.CalledProcessError as e:
                print(f"[!] Error en {os.path.basename(script)}: {e.stderr.decode()}")
    
    print("[*] Metamorfosis completada exitosamente.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python metamorphosis.py <InstanceName> <HostName>")
    else:
        perform_metamorphosis(sys.argv[1], sys.argv[2])
