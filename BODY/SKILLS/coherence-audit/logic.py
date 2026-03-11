import os
import json
import sys
from pathlib import Path

def get_root():
    return Path(__file__).resolve().parents[3]

ROOT = get_root()

def audit_roadmap():
    print("--- [AUDIT] Verificando Roadmap de la Semilla ---")
    roadmap_path = ROOT / "PROYECTOS" / "Evolucion_Terroir" / "Holisto_Seed" / "ROADMAP.md"
    if not roadmap_path.exists():
        print("[!] ERROR: No se encuentra ROADMAP.md")
        return False

    with open(roadmap_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if "## 🟢 Phase 4: Full Autonomy & Release [IN PROGRESS]" in content and "- [ ]" in content.split("## 🟢 Phase 2")[1]:
            print("[!] INCONSISTENCIA: Fase 4 en progreso pero Fase 2 tiene pendientes.")
    return True

def audit_projects_index():
    print("--- [AUDIT] Verificando Índice de Proyectos (Criterio HOL-ARC-014) ---")
    index_path = ROOT / "proyectos" / "gemini.md"
    if not index_path.exists():
        print("[!] ERROR: No se encuentra proyectos/gemini.md")
        return False

    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            projects = data.get("content", {}).get("projects", [])
            for p in projects:
                path = ROOT / p.get("path", "")
                cat_id = p.get("category_id", "")
                remote = p.get("remote_url")
                
                exists = path.exists()
                
                if exists:
                    print(f"[+] Proyecto '{p['name']}' verificado en disco.")
                else:
                    if cat_id == "terroir-evo":
                        print(f"[!] ERROR CRÍTICO: El proyecto obligatorio '{p['name']}' NO existe en {path}")
                    elif remote:
                        print(f"[~] ESTADO POTENCIAL: Proyecto '{p['name']}' ausente en disco pero disponible en {remote}")
                    else:
                        print(f"[!] FRICCIÓN: El proyecto '{p['name']}' no existe y no tiene puntero remoto.")
    except Exception as e:
        print(f"[!] Error al parsear el índice: {str(e)}")
    return True

def run_full_audit():
    print("=== Iniciando Auditoría de Coherencia (PCD v1.1) ===")
    r1 = audit_roadmap()
    r2 = audit_projects_index()
    print("=== Auditoría Finalizada. ===")

if __name__ == "__main__":
    run_full_audit()
