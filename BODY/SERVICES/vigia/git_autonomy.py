import subprocess
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa si el PYTHONPATH no esta configurado
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

# Configuración de logging específica para este módulo
logger = logging.getLogger("git_autonomy")

class GitAutonomy:
    """
    Módulo de 'Exhalación' para El Vigía.
    Encargado de persistir los cambios generados por el bot (agenda, notificaciones, logs)
    en el repositorio remoto, asegurando la sincronización del Terroir.
    """
    
    def __init__(self, repo_path=None):
        self.repo_path = repo_path or TerroirLocator.get_orchestrator_root()
        self._ensure_identity()

    def _ensure_identity(self):
        """Verifica si hay identidad git configurada; si no, asigna una de oficio."""
        ok, email = self._run_git_command(["config", "user.email"])
        if not ok or not email:
            logger.warning("Identidad Git no detectada. Asignando 'Identidad de Oficio' local.")
            self._run_git_command(["config", "user.email", "vigia@holisto.ai"])
            self._run_git_command(["config", "user.name", "El Vigia (Automata)"])

    def _run_git_command(self, args):
        """Ejecuta un comando git y maneja errores básicos."""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = f"Error ejecutando 'git {' '.join(args)}': {e.stderr.strip()}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            logger.error(f"Error inesperado en git: {str(e)}")
            return False, str(e)

    def push_changes(self, commit_message=None):
        """
        Ciclo de Exhalación: Pull (Rebase) -> Add -> Commit -> Push.
        Intenta sincronizar los cambios locales con el remoto.
        """
        if commit_message is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            commit_message = f"Vigia Autonomy: Actualización automática [{timestamp}]"

        logger.info("Iniciando ciclo de exhalación (Push)...")

        # Rutas Agnosticas
        phenotype_root = TerroirLocator.get_phenotype_root()
        mem_root = TerroirLocator.get_mem_root()

        # 1. Inhalación preventiva (Pull --rebase)
        logger.info("Intentando inhalación preventiva (Pull --rebase)...")
        
        handover_path = mem_root / "handover_vigia.json"
        if handover_path.exists():
            logger.info("Testamento de vigilia detectado. Asegurando rastreo preventivo...")
            self._run_git_command(["add", str(handover_path)])

        ok, msg = self._run_git_command(["pull", "--rebase"])
        if not ok:
            if "untracked working tree files would be overwritten" in msg:
                logger.warning("Conflicto residual detectado por archivos untracked. Intentando integración forzada total...")
                self._run_git_command(["add", "."])
                ok, msg = self._run_git_command(["pull", "--rebase"])
            
            if not ok:
                logger.error(f"Fallo crítico en pull: {msg}. Abortando rebase si existe.")
                self._run_git_command(["rebase", "--abort"])

        # 2. Add (Staging) Quirúrgico usando rutas agnósticas
        safe_paths = [
            phenotype_root / "SYSTEM" / "AGENDA",
            phenotype_root / "SYSTEM" / "NOTIFICACIONES",
            mem_root / "logs_vigia",
            phenotype_root / "SYSTEM" / "NOTAS_VIGIA",
            phenotype_root / "SYSTEM" / "MAPA_DEL_TERROIR" / "GEMINI.md",
            mem_root / "GEMINI.md",
            mem_root / "handover_vigia.json"
        ]
        
        logger.info("Preparando exhalación selectiva de componentes operativos...")
        for path in safe_paths:
            if path.exists():
                self._run_git_command(["add", str(path)])

        # 3. Commit
        ok, status_msg = self._run_git_command(["status", "--porcelain"])
        if not ok or not status_msg:
            logger.info("Nada que exhalar (sin cambios pendientes).")
            return True

        ok, msg = self._run_git_command(["commit", "-m", commit_message])
        if not ok: return False
        
        # 4. Push
        ok, msg = self._run_git_command(["push"])
        if ok:
            logger.info("Exhalación exitosa: Cambios sincronizados con el Terroir.")
            return True
        else:
            logger.error(f"Fallo en la exhalación (Push): {msg}")
            return False
