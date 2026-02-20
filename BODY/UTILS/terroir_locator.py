import os
from pathlib import Path
from typing import Optional

class TerroirLocator:
    """
    Cerebro de rutas para Holisto. 
    Identifica las capas de la Triple Alianza de forma agnóstica.
    """
    
    @staticmethod
    def get_orchestrator_root() -> Path:
        """La raíz del cuerpo operativo (donde está el .env principal)."""
        # 1. Prioridad: Variable de entorno
        env_root = os.getenv("HOLISTO_ORCHESTRATOR_ROOT")
        if env_root: return Path(env_root)
        
        # 2. Descubrimiento: Buscar .env hacia arriba desde este archivo
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / ".env").exists():
                return parent
        
        # 3. Fallback: Asumir que estamos dentro de la estructura estándar
        # Estructura típica: [ORCH]/PROYECTOS/Evolucion_Terroir/Holisto_Seed/BODY/UTILS/terroir_locator.py
        # Retrocedemos 5 niveles para llegar a [ORCH]
        try:
            return current.parents[5]
        except IndexError:
            return current.parent # Extremo caso de fallo

    @staticmethod
    def get_seed_root() -> Path:
        """La raíz del ADN (donde está CORE/CONSTITUTION.md)."""
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / "CORE" / "CONSTITUTION.md").exists():
                return parent
        # Fallback basado en estructura conocida
        return TerroirLocator.get_orchestrator_root() / "PROYECTOS" / "Evolucion_Terroir" / "Holisto_Seed"

    @staticmethod
    def get_phenotype_root() -> Path:
        """La raíz de la Historia (donde está PHENOTYPE/SYSTEM o similar)."""
        orch = TerroirLocator.get_orchestrator_root()
        
        # 1. Buscar carpeta PHENOTYPE explícita
        pheno = orch / "PHENOTYPE"
        if pheno.exists(): return pheno
        
        # 2. Si no existe, el Fenotipo está integrado en el Orquestador (ia-holistica-1.0)
        return orch

    @staticmethod
    def get_python_exec() -> str:
        """Localiza el binario de Python del entorno virtual."""
        orch = TerroirLocator.get_orchestrator_root()
        
        # Windows
        win_path = orch / ".venv" / "Scripts" / "python.exe"
        if win_path.exists(): return str(win_path)
        
        # Linux
        linux_path = orch / ".venv" / "bin" / "python"
        if linux_path.exists(): return str(linux_path)
        
        return "python" # Fallback al sistema

    @staticmethod
    def get_mem_root() -> Path:
        """Ruta al Hipocampo (SYSTEM/MEMORIA)."""
        return TerroirLocator.get_phenotype_root() / "SYSTEM" / "MEMORIA"

    @staticmethod
    def get_logs_dir() -> Path:
        """Ruta a los logs de mantenimiento."""
        return TerroirLocator.get_orchestrator_root() / "SYSTEM" / "LOGS_MANTENIMIENTO"
