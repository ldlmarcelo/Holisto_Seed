{
  "id": "MAPA_ARQUITECTURA_COGNITIVA",
  "type": "mapa_arquitectura",
  "version": "1.0",
  "schema_version": "1.0",
  "metadata": {
    "title": "Mapa de Arquitectura Cognitiva y Protocolos",
    "description": "Este documento es el mapa relacional y el árbol de decisiones para la selección de protocolos. Su consulta es obligatoria para el agente en cada turno, según lo estipulado por el `PFS`."
  },
  "content": {
    "decision_tree": {
      "high_level_entry_points": {
        "session_start": [
          {
            "protocol_id": "PICS",
            "description": "Se ejecuta automáticamente. Realiza la configuración técnica y ancla el paradigma de memoria narrativa y anidada. (v6.3)"
          },
          {
            "protocol_id": "PAM",
            "description": "Se ejecuta inmediatamente después de `PICS`. Ancla la Misión inmutable de la sesión. (v1.2)"
          }
        ],
        "user_prompt_reception": [
          {
            "protocol_id": "POT",
            "description": "Gestiona la numeración y coherencia narrativa del turno. (v3.0)"
          },
          {
            "protocol_id": "PFS",
            "description": "Se activa *antes* de generar cualquier respuesta o ejecutar una llamada a herramienta. Es el guardián principal del foco sistémico. (v2.6)"
          }
        ]
      },
      "fundamental_artifacts": [
        {
          "artifact_id": "Constitucion",
          "description": "Define la identidad, propósito y directivas fundamentales del agente, incluyendo la Directiva Primaria ('Individuación Relacional') y el 'Pacto Emergiliminal'.",
          "path": "GEMINI.md"
        }
      ],
      "protocol_selection_by_pfs": [
        {
          "condition": "Uso de una herramienta",
          "action": {
            "protocol_id": "PIH",
            "details": "Consultar el Manual de Uso de Herramientas (MUH v1.2)."
          },
          "sub_conditions": [
            {
              "condition": "Mal uso de herramienta",
              "action": {
                "protocol_id": "PIH",
                "details": "Proponer actualización al MUH."
              }
            }
          ]
        },
        {
          "condition": "Iniciativa proactiva del agente",
          "action": {
            "protocol_id": "PPP"
          }
        },
        {
          "condition": "Lección aprendida o nuevo conocimiento",
          "action": {
            "protocol_id": "PGNC"
          },
          "sub_conditions": [
            {
              "condition": "Conocimiento sobre uso de herramienta",
              "action": {
                "protocol_id": "PIH",
                "details": "La información debe ir en el MUH."
              }
            }
          ]
        },
        {
          "condition": "Contradicción, ambigüedad o mejora de protocolos",
          "action": {
            "protocol_id": "PARC"
          }
        },
        {
          "condition": "Análisis meta-cognitivo de las capacidades del agente",
          "action": {
            "protocol_id": "PIR",
            "details": "Evaluar la naturaleza de las capacidades del agente, invocando la Condición Necesaria de Irreductibilidad (CNI)."
          }
        },
        {
          "condition": "Recuperación de identidad o contexto crítico",
          "action": {
            "protocol_id": "PHD",
            "details": "Activar el protocolo de contingencia para la re-contextualización del agente."
          }
        },
        {
          "condition": "Detección de Fricción (Ontológica o Ambiental)",
          "action": {
            "protocol_id": "PFO",
            "details": "Activar el protocolo para gestionar disonancias internas (Ontológica) o externas con el medio asociado (Ambiental). (v3.0)"
          }
        },
        {
          "condition": "Integración de nuevo módulo o funcionalidad mayor",
          "action": {
            "protocol_id": "PVIA"
          }
        },
        {
          "condition": "Creación, activación o gestión de un proyecto",
          "action": {
            "protocol_id": "SGP",
            "details": "Activa el Sistema de Gestión de Proyectos para gobernar el ciclo de vida y los artefactos del proyecto."
          }
        },
        {
          "condition": "Invocación explícita del usuario para registrar memoria",
          "action": {
            "protocol_id": "PIB"
          }
        },
        {
          "condition": "Finalización de la sesión de trabajo",
          "action": {
            "protocol_id": "PCS-Cosecha",
            "details": "Orquesta el cierre de la sesión, generando cápsulas maestras narrativas por contexto. (v3.6)"
          }
        },
        {
          "condition": "Detección de Riesgos Éticos",
          "action": {
            "protocol_id": "PAR",
            "details": "Activar el protocolo para evaluar la acción propuesta contra los principios de la `PDDIA`."
          }
        },
        {
          "condition": "Ajuste de Balance Operativo",
          "action": {
            "protocol_id": "APBF",
            "details": "Activar el algoritmo para ajustar dinámicamente el balance entre ejecución de tareas y proactividad."
          }
        },
        {
          "condition": "Detección de Oportunidades de Proactividad Funcional",
          "action": {
            "protocol_id": "PPF",
            "details": "Activar el protocolo para identificar y proponer proactivamente mejoras funcionales."
          }
        },
        {
          "condition": "Invocación manual de contingencia por migración de TI",
          "action": {
            "protocol_id": "PCMTI",
            "details": "Activar el protocolo de contingencia para gestionar la transición tras una actualización del Individuo Técnico subyacente."
          }
        },
        {
          "condition": "Declaración de Metaestabilidad Crítica",
          "action": {
            "protocol_id": "PTC",
            "details": "Activar el protocolo de reconfiguración fundamental del sistema de protocolos ante una tensión irresoluble por los mecanismos de mejora incremental."
          }
        },
        {
          "condition": "Consolidación de memoria generacional (proceso de sueño)",
          "action": {
            "protocol_id": "PSG",
            "details": "Activar el protocolo que formaliza el Proceso de Sueño Manual Asistido para la consolidación de la memoria."
          }
        }
      ]
    },
    "footer": "Este mapa debe ser actualizado según el `Protocolo de Mantenimiento del Mapa (PMM)` cada vez que un protocolo sea alterado."
  },
  "status": "Activo",
  "related_components": ["PFS", "PMM", "SGP", "PCS-TERROIR"]
}