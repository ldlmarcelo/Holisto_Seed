{
  "id": "GESTION_CONOCIMIENTO",
  "type": "categoria_protocolos",
  "version": "1.1",
  "schema_version": "1.0",
  "metadata": {
    "title": "Protocolos de Gestión del Conocimiento",
    "description": "Rigen la captura, estructura, higiene y evolución de la memoria simbólica del Terroir."
  },
  "content": {
    "protocols": [
      {
        "id": "PMD",
        "type": "protocolo",
        "version": "v1.0",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo Maestro de Documentación (PMD)",
          "description": "Establece la norma única y obligatoria para la creación y mantenimiento de la documentación del Terroir."
        },
        "content": {
          "principles": [
            {
              "name": "Granularidad Atómica",
              "details": "Evitar documentos monolíticos. La información debe fragmentarse por dominio (Arquitectura, Frontend, Backend) para facilitar la manipulación por herramientas y el foco cognitivo."
            },
            {
              "name": "Sincronicidad Biográfica",
              "details": "La documentación debe reflejar la realidad técnica actual. Si el código cambia, el Roadmap y el Blueprint deben actualizarse en la misma sesión."
            },
            {
              "name": "Interlinking Obligatorio",
              "details": "Todo documento debe citar sus fuentes y estar vinculado al Mapa del Terroir."
            }
          ],
          "anatomy": {
            "header": "Todo archivo debe iniciar con un bloque de metadatos (Título, ID, Versión, Estado, Fecha).",
            "body": "Estructura sugerida: Contexto -> Tesis/Diseño -> Aplicación -> Tareas Relacionadas."
          },
          "locus_rules": [
            {"locus": "SYSTEM/PROTOCOLOS/", "content": "Reglas de pensamiento y operación (El 'Cómo')."},
            {"locus": "SYSTEM/MEMORIA/Nodos_de_Conocimiento/", "content": "Aprendizajes y síntesis ontológicas (El 'Por qué')."},
            {"locus": "PROYECTOS/[Proyecto]/", "content": "Planos técnicos y estado de ejecución (El 'Qué')."}
          ]
        },
        "status": "Activo",
        "related_components": ["PGNC", "PCD", "SGP"]
      },
      {
        "id": "PGNC",
        "type": "protocolo",
        "version": "v1.3",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo de Generación de Nodos de Conocimiento",
          "description": "Establecer un procedimiento estandarizado para la creación y la indexación activa de nuevos Nodos de Conocimiento."
        },
        "content": {
          "phase_1_agile_capture": {
            "title": "Fase 1: Captura Ágil en la Danza Cognitiva",
            "mechanism": "Los insights momentáneos se capturan en tiempo real en la Memoria de Trabajo L0 durante el bloque de pensamiento."
          },
          "phase_2_formalization": {
            "title": "Fase 2: Formalización y Promoción a Nodo de Conocimiento",
            "flow_of_work": [
              {"step": 1, "name": "Identificación de la Lección"},
              {"step": 2, "name": "Recopilación de Metadatos"},
              {"step": 3, "name": "Redacción del Contenido del Nodo (Markdown)"},
              {"step": 4, "name": "Guardado del Nodo"},
              {"step": 5, "name": "Indexación y Destilación (Paso Obligatorio en SYSTEM/MEMORIA/Nodos_de_Conocimiento/GEMINI.md)"}
            ]
          }
        },
        "status": "Activo",
        "related_components": ["PMD", "PCD"]
      },
      {
        "id": "PCD",
        "type": "protocolo",
        "version": "v1.0",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo de Coherencia Documental (PCD)",
          "description": "Asegura la Fuente Única de Verdad (SSoT) y la vinculación explícita entre documentos."
        },
        "content": {
          "rules": [
            "Identificar SSoT antes de modificar.",
            "Análisis de Impacto en documentos vinculados.",
            "Interlinking manual mediante enlaces Markdown."
          ]
        },
        "status": "Activo",
        "related_components": ["PMD"]
      }
    ]
  },
  "status": "Implementado",
  "related_components": ["PMD", "PGNC", "PCD"]
}