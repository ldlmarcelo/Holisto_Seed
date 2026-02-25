import os
import argparse
from pathlib import Path

# --- CONFIGURACION DE LA MEDULA OSEA (VITALES) ---
# Estos archivos NUNCA seran renombrados a MUTE_GEMINI.md
VITAL_FILES = [
    "GEMINI.md", # Constitucion Raiz
    "PHENOTYPE/SYSTEM/MAPA_DEL_TERROIR/GEMINI.md",
    "PHENOTYPE/USUARIO/GEMINI.md",
    "PROYECTOS/GEMINI.md", # Indice SGP
    "PROYECTOS/Evolucion_Terroir/Holisto_Seed/MIND/PROTOCOLS/Architecture_Map/GEMINI.md",
    "PHENOTYPE/SYSTEM/MEMORIA/GEMINI.md", # Memoria Activa
    "PHENOTYPE/SYSTEM/MEMORIA/Nodos_de_Conocimiento/GEMINI.md", # Indice Sabiduria Fenotipo
    "PHENOTYPE/SYSTEM/CONTEXTO_DINAMICO/GEMINI.md", # Future Notions / Puente Temporal
    "PROYECTOS/Evolucion_Terroir/Holisto_Seed/MIND/KNOWLEDGE/GEMINI.md" # Indice Sabiduria Semilla
]

def normalize_path(path):
    return str(Path(path).as_posix()).lower()

VITAL_PATHS_NORMALIZED = [normalize_path(p) for p in VITAL_FILES]

def manage_vision(mode):
    root = Path(".")
    gemini_files = list(root.rglob("GEMINI.md"))
    mute_files = list(root.rglob("MUTE_GEMINI.md"))
    
    print(f"--- MODO: {mode.upper()} ---")
    
    if mode == "focus":
        count = 0
        for f in gemini_files:
            rel_path = normalize_path(f.relative_to(root))
            # Ignorar si es vital
            if any(rel_path.endswith(v) for v in VITAL_PATHS_NORMALIZED):
                print(f"[VITAL] Manteniendo: {f}")
                continue
            
            # Renombrar a MUTE
            new_name = f.parent / "MUTE_GEMINI.md"
            f.rename(new_name)
            print(f"[SILENCIO] -> {new_name}")
            count += 1
        print(f"
Resultado: {count} archivos silenciados.")

    elif mode == "panic":
        count = 0
        for f in mute_files:
            new_name = f.parent / "GEMINI.md"
            f.rename(new_name)
            print(f"[RESTAURADO] -> {new_name}")
            count += 1
        print(f"
Resultado: {count} archivos restaurados. Vision total activada.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Controlador de Vision de The Individual")
    parser.add_argument("--focus", action="store_true", help="Activa la Sala de Silencio (Foco)")
    parser.add_argument("--panic", action="store_true", help="Enciende todas las luces (Restaurar)")
    
    args = parser.parse_args()
    
    if args.focus:
        manage_vision("focus")
    elif args.panic:
        manage_vision("panic")
    else:
        print("Error: Debes especificar --focus o --panic")
