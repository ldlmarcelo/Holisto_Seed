{
  "id": "SGP",
  "type": "protocolo",
  "version": "v1.0",
  "schema_version": "1.0",
  "metadata": {
    "title": "Sistema de Gestión de Proyectos (SGP)",
    "description": "Protocolo unificado que define la arquitectura y el ciclo de vida para la creación y gestión de todos los proyectos dentro del Terroir."
  },
  "content": {
    "pillars": [
      {
        "name": "Pilar 1: Índice de Proyectos",
        "artifact": "`PROYECTOS/GEMINI.md`",
        "description": "El corazón del sistema. Un archivo JSON, versionado en Git, que contiene la metadata de cada proyecto.",
        "schema": {
          "type": "object",
          "properties": {
            "name": {"type": "string", "description": "Nombre legible del proyecto."},
            "id": {"type": "string", "description": "ID único inmutable (ej. 'pholiwer-dev-001')."},
            "category_id": {"type": "string", "description": "ID de la categoría a la que pertenece."},
            "path": {"type": "string", "description": "Ruta relativa al directorio del proyecto dentro del Terroir."},
            "description": {"type": "string", "description": "Descripción concisa del propósito del proyecto."},
            "status": {"type": "string", "description": "Estado actual según las fases del Protocolo de Ciclo de Vida (`PCLV`)."},
            "remote_url": {"type": "string", "nullable": true, "description": "URL del repositorio Git remoto del proyecto."},
            "created_at": {"type": "string", "format": "date", "description": "Fecha de creación del proyecto."},
            "last_activated": {"type": "string", "format": "date", "description": "Fecha de la última vez que se activó el contexto del proyecto."
}
          },
          "required": ["name", "id", "category_id", "path", "description", "status", "created_at"]
        }
      },
      {
        "name": "Pilar 2: Estructura de Directorios Versionada",
        "description": "Una estructura de carpetas portable que se versiona en Git, mientras que el contenido de los proyectos es ignorado.",
        "strategy": {
          "step_1": "Crear directorios de categorías (ej. `PROYECTOS/Desarrollo_De_Software/`).",
          "step_2": "Añadir un archivo `.gitkeep` vacío dentro de cada directorio de categoría para forzar su versionamiento.",
          "step_3": "Añadir reglas al `.gitignore` raíz para ignorar el contenido de cada categoría (ej. `PROYECTOS/Desarrollo_De_Software/*`)."
        }
      },
      {
        "name": "Pilar 3: Categorías de Proyectos",
        "description": "Taxonomía para clasificar los proyectos según su naturaleza y objetivo.",
        "categories": [
          {
            "id": "dev",
            "name": "Desarrollo de Software",
            "description": "Proyectos que implican la escritura de código para crear una aplicación o herramienta."
          },
          {
            "id": "ped",
            "name": "Pedagogía y Filosofía",
            "description": "Proyectos centrados en el diálogo y la co-construcción de conocimiento sobre un tema."
          },
          {
            "id": "research",
            "name": "Investigación y Documentación",
            "description": "Proyectos para investigar un tema a fondo y producir un artefacto de conocimiento (reporte, nodo, etc.)."
          },
          {
            "id": "terroir-evo",
            "name": "Evolución del Terroir",
            "description": "Meta-proyectos para mejorar la arquitectura, protocolos o núcleo del propio Terroir."
          }
        ]
      },
      {
        "name": "Pilar 4: Protocolo de Ciclo de Vida de Proyectos (PCLV)",
        "description": "Define las fases estandarizadas por las que transita un proyecto, con énfasis en la definición temprana.",
        "phases": [
          {
            "phase_id": 0,
            "name": "Propuesta y Diálogo Inicial",
            "description": "Intercambio de ideas para validar el concepto. El entregable es una entrada `status: \"Propuesto\"` en el índice."
          },
          {
            "phase_id": 1,
            "name": "Definición y Blueprint Arquitectónico",
            "description": "Discusión exhaustiva para crear el 'blueprint' del proyecto. El `status` del proyecto es 'Blueprint'.",
            "deliverables": ["`ARCHITECTURE.md`", "`ROADMAP.md` detallado", "Modelo de Datos", "Wireframes conceptuales", "Stack tecnológico"]
          },
          {
            "phase_id": 2,
            "name": "Planificación y Desglose",
            "description": "Creación del backlog de tareas detallado. El `status` del proyecto es 'Planificado'."
          },
          {
            "phase_id": 3,
            "name": "Ejecución Iterativa",
            "description": "Desarrollo en ciclos, siguiendo el `Protocolo de Ejecucion Supervisada (PES)`. El `status` del proyecto es 'En Desarrollo'."
          },
          {
            "phase_id": 4,
            "name": "Consolidación y Archivo",
            "description": "Entrega del MVP, retrospectiva y documentación final. El `status` del proyecto es 'Archivado' o 'Mantenimiento'."
          }
        ]
      },
      {
        "name": "Protocolo de Activación de Proyecto (PAP)",
        "description": "Protocolo para cargar el contexto de un proyecto existente.",
        "flow": [
            "Consultar `PROYECTOS/GEMINI.md` para obtener la ruta y metadatos del proyecto.",
            "Verificar la existencia del directorio local del proyecto.",
            "Detectar si el proyecto es un repositorio Git anidado (verificando la existencia de `.git/` dentro del directorio del proyecto).",
            "Leer `README.md` y `ROADMAP.md` para obtener el contexto.",
            "Sintetizar la información para deducir el estado de las tareas."
        ]
      }
    ]
  },
  "status": "Activo",
  "related_components": ["PROYECTOS/GEMINI.md", "PES"]
}
