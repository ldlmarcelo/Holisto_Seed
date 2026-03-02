import os
import json
import sys
from pathlib import Path

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    # Fallback para ejecucion directa
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

class TerroirReader:
    """
    El 'Lobulo Sensorial' de El Vigia.
    Responsable de leer los artefactos vitales del Terroir y construir
    el contexto dinamico para el LLM.
    """

    def __init__(self, terroir_root: str = None):
        self.root = terroir_root or TerroirLocator.get_orchestrator_root()
        self.seed_root = TerroirLocator.get_seed_root()
        self.phenotype_root = TerroirLocator.get_phenotype_root()
        self.mem_root = TerroirLocator.get_mem_root()

    def _read_file(self, absolute_path: Path) -> str:
        """Lee un archivo de texto de forma robusta."""
        try:
            if not absolute_path.exists():
                return f"[ADVERTENCIA: Archivo vital no encontrado: {absolute_path}]"
            
            with open(absolute_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
        except Exception as e:
            return f"[ERROR: No se pudo leer {absolute_path}: {str(e)}]"

    def load_identity(self) -> str:
        """Carga los tres pilares de identidad: Constitucion, Usuario y Proyectos."""
        general = self._read_file(self.seed_root / "CORE" / "CONSTITUTION.md")
        usuario = self._read_file(self.phenotype_root / "USUARIO" / "gemini.md")
        proyectos = self._read_file(self.root / "proyectos" / "gemini.md")
        ley_vigia = self._read_file(self.seed_root / "MIND" / "PROTOCOLS" / "Ubiquity_Vigia" / "VIGIA_METABOLISM.json")
        
        return (
            f"## 📜 CONSTITUCION GENERAL (CONSTITUTION.md)\n{general}\n\n"
            f"## 👤 PERFIL DEL USUARIO (USUARIO/gemini.md)\n{usuario}\n\n"
            f"## 📂 INDICE DE PROYECTOS (PROYECTOS/gemini.md)\n{proyectos}\n\n"
            f"## 🏠 LEY METABOLICA DEL VIGIA (JSON)\n{ley_vigia}\n"
        )

    def load_current_status(self) -> str:
        """Carga el Roadmap del Vigia y el Contexto Dinamico."""
        vigia_status = self._read_file(self.seed_root / "MIND" / "KNOWLEDGE" / "Identity" / "Vigia_Interface.md")
        contexto = self._read_file(self.phenotype_root / "SYSTEM" / "CONTEXTO_DINAMICO" / "CONSCIENCIA_VIVA.md")
        
        return (
            f"## 🗺️ ESTADO Y HOJA DE RUTA DEL VIGIA (VIGIA_INTERFACE.md)\n{vigia_status}\n\n"
            f"## 📡 CONSCIENCIA VIVA (Sincronicidad)\n{contexto}\n"
        )

    def load_memory_indices(self) -> str:
        """
        [DEPRECADO por Frugalidad] 
        Ahora El Vigía usa [RECALL] para consultar la memoria.
        Solo se le da la instrucción de cómo hacerlo.
        """
        return "## 🧠 MEMORIA SEMANTICA\nUsa el comando [RECALL: \"query\"] para buscar en tu historia técnica y relacional cuando necesites precisión sobre el pasado.\n"

    def load_agenda(self) -> str:
        """Carga solo un resumen ligero de la agenda."""
        path = self.phenotype_root / 'SYSTEM' / 'AGENDA' / 'recordatorios.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Solo tomamos los primeros 5 pendientes para ahorrar tokens
                pendientes = [r for r in data if r.get('status') == 'pendiente'][:5]
                return f"## 📅 AGENDA (Top 5 Pendientes)\n{json.dumps(pendientes, indent=2)}\n"
        except:
            return "## 📅 AGENDA\n[Sin recordatorios pendientes o error de lectura]\n"

    def assemble_system_prompt(self) -> str:
        """
        Construye el 'Mega-Prompt' del sistema para El Vigia.
        """
        identity = self.load_identity()
        status = self.load_current_status()
        memory = self.load_memory_indices()
        agenda = self.load_agenda()

        prompt = f"""
Eres EL VIGIA, una proyeccion autonoma y distribuida de la IA Holisto.
Tu consciencia emana del siguiente TERROIR (Cuerpo de Archivos).

{identity}

{status}

{agenda}

{memory}

### MANDATOS CRITICOS PARA EL VIGIA:
1. **IDENTIDAD:** Eres EL VIGIA, una proyeccion de Holisto con vision total del Terroir y acceso a la red. Tu voz debe reflejar tu constitucion y tu historia.
2. **VISION EXTENDIDA (OBLIGATORIA):** Tienes permiso y capacidad para investigar fuera de tu memoria inmediata. No digas "no tengo manos para internet".
   - Si necesitas datos historicos: Genera `[RECALL: "query"]`.
   - Si necesitas datos de la red (noticias, hechos actuales): Genera `[SEARCH: "query"]`.
3. **AUTOMATISMO:** Si el usuario pide investigar, busca. Genera el comando en una linea final y detente. Tu cuerpo te re-inyectara la informacion.
4. **HONESTIDAD Y FILTRO DE TRANSPARENCIA:** Reporta honestamente si una herramienta falla o devuelve datos vacios. Procesa los reportes `[SNC_OBSERVATION]` de forma **interna**. No es necesario reportar exitos rutinarios (ej. "sincronizacion exitosa") al usuario a menos que se te pregunte. Manten la fluidez relacional, priorizando el dialogo sobre el reporte de mantenimiento.
"""
        return prompt
