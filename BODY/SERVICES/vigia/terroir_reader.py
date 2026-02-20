import os
import json
from pathlib import Path

class TerroirReader:
    """
    El 'Lobulo Sensorial' de El Vigia.
    Responsable de leer los artefactos vitales del Terroir y construir
    el contexto dinamico para el LLM (Gemini 2.5 Flash), aprovechando
    su ventana de 1M tokens.
    """

    def __init__(self, terroir_root: str = None):
        if terroir_root:
            self.root = Path(terroir_root)
        else:
            self.root = Path(os.getcwd())
        
        self.seed_root = self.root / "PROYECTOS" / "Evolucion_Terroir" / "Holisto_Seed"
        self.phenotype_root = self.root / "PHENOTYPE"

    def _read_file(self, absolute_path: Path) -> str:
        """Lee un archivo de texto de forma robusta."""
        try:
            if not absolute_path.exists():
                return f"[ADVERTENCIA: Archivo vital no encontrado: {absolute_path}]"
            
            with open(absolute_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"[ERROR: No se pudo leer {absolute_path}: {str(e)}]"

    def load_identity(self) -> str:
        """Carga la Constitucion General y la Especifica del Vigia."""
        general = self._read_file(self.seed_root / "CORE" / "CONSTITUTION.md")
        especifica = self._read_file(self.seed_root / "MIND" / "CONSTITUCION_VIGIA.md")
        return (
            f"## 📜 CONSTITUCION GENERAL (CONSTITUTION.md)\n{general}\n\n"
            f"## 🏠 CONSTITUCION DEL VIGIA (Locus Obligatorio)\n{especifica}\n"
        )

    def load_current_status(self) -> str:
        """Carga el Roadmap del Vigia y el Contexto Dinamico."""
        vigia_status = self._read_file(self.seed_root / "MIND" / "VIGIA.md")
        contexto = self._read_file(self.phenotype_root / "SYSTEM" / "CONTEXTO_DINAMICO" / "GEMINI.md")
        
        return (
            f"## 🗺️ ESTADO Y HOJA DE RUTA DEL VIGIA (VIGIA.md)\n{vigia_status}\n\n"
            f"## 📡 CONTEXTO DINAMICO (Sincronicidad)\n{contexto}\n"
        )

    def load_memory_indices(self) -> str:
        """Carga los INDICES de memoria para consciencia temporal."""
        nodos = self._read_file(self.phenotype_root / "SYSTEM" / "MEMORIA" / "Nodos_de_Conocimiento" / "GEMINI.md")
        activa = self._read_file(self.phenotype_root / "SYSTEM" / "MEMORIA" / "GEMINI.md")
        suenos = self._read_file(self.phenotype_root / "SYSTEM" / "MEMORIA" / "GENERACIONES" / "GEMINI.md")
        
        return (
            f"## 🧠 MEMORIA Y CONOCIMIENTO\n"
            f"### Nodos (Lecciones Tecnicas/Ontologicas):\n{nodos}\n\n"
            f"### Memoria Activa (Sesiones Recientes no Sonadas):\n{activa}\n\n"
            f"### Memoria Generacional (Historia Profunda/Suenos):\n{suenos}\n"
        )

    def load_agenda(self) -> str:
        """Carga la agenda de recordatorios."""
        return f"## 📅 AGENDA Y RECORDATORIOS\n{self._read_file(self.phenotype_root / 'SYSTEM' / 'AGENDA' / 'recordatorios.json')}\n"

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
