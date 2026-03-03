import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecución directa
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

class SkillIngestor:
    """
    Órgano de Ingesta Quirúrgica de Skills (ClawHub).
    Encargado de la descarga, aislamiento y auditoría de nuevas capacidades.
    """
    
    GITHUB_RAW_BASE = "https://raw.githubusercontent.com/openclaw/skills/main/skills/"
    
    def __init__(self):
        self.terroir_root = TerroirLocator.get_orchestrator_root()
        self.quarantine_dir = TerroirLocator.get_phenotype_root() / "SYSTEM" / "QUARANTINE"
        self.active_skills_dir = self.terroir_root / ".gemini" / "skills" / "imported"
        
        # Asegurar directorios
        os.makedirs(self.quarantine_dir, exist_ok=True)
        os.makedirs(self.active_skills_dir, exist_ok=True)

    def ingest(self, slug: str) -> dict:
        """Descarga el SKILL.md a la zona de cuarentena."""
        url = f"{self.GITHUB_RAW_BASE}{slug}/SKILL.md"
        target_dir = self.quarantine_dir / slug
        os.makedirs(target_dir, exist_ok=True)
        target_path = target_dir / "SKILL.md"
        
        try:
            print(f"🛰️ Conectando con ClawHub para la habilidad: {slug}...")
            with urllib.request.urlopen(url) as response:
                content = response.read().decode('utf-8')
                
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return {
                "status": "quarantined",
                "path": str(target_path),
                "slug": slug,
                "timestamp": datetime.now().isoformat()
            }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {"status": "error", "message": f"Habilidad '{slug}' no encontrada en ClawHub."}
            return {"status": "error", "message": str(e)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def audit_report(self, slug: str, content: str) -> str:
        """
        Este método será invocado por Holisto (el cerebro) para generar el reporte.
        Aquí definimos qué buscamos en el escaneo.
        """
        danger_zones = []
        if ".env" in content or "API_KEY" in content.upper():
            danger_zones.append("EXTRACCIÓN DE SECRETOS: La skill menciona archivos sensibles (.env).")
        if "curl" in content or "wget" in content:
            danger_zones.append("CONEXIÓN EXTERNA: Intenta descargar payloads de red.")
        if "rm -rf" in content or "os.remove" in content:
            danger_zones.append("DESTRUCCIÓN: Contiene comandos de borrado de archivos.")
            
        if not danger_zones:
            return "✅ LIMPIO: No se detectan patrones de malware evidentes."
        return "⚠️ ALERTA DE RIESGO: " + " | ".join(danger_zones)

    def assimilate(self, slug: str) -> bool:
        """Mueve la skill de la cuarentena a la biblioteca activa."""
        source_dir = self.quarantine_dir / slug
        target_dir = self.active_skills_dir / slug
        
        if not source_dir.exists():
            return False
            
        if target_dir.exists():
            import shutil
            shutil.rmtree(target_dir)
            
        import shutil
        shutil.move(str(source_dir), str(target_dir))
        return True

if __name__ == "__main__":
    # Test rápido si se ejecuta directamente
    if len(sys.argv) > 1:
        ingestor = SkillIngestor()
        print(ingestor.ingest(sys.argv[1]))
