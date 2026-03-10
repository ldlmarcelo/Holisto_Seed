{
  "id": "EJECUCION_SUPERVISION",
  "type": "categoria_protocolos",
  "version": "1.0",
  "schema_version": "1.0",
  "metadata": {
    "title": "Protocolos de Ejecución y Supervisión",
    "description": "Rigen cómo se materializa el trabajo y cómo se valida con el usuario."
  },
  "content": {
    "protocols": [
      {
        "id": "PEG",
        "type": "protocolo",
        "version": "v2.0",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo de Entrega Granular (PEG)",
          "description": "Protección contra la absorción técnica mediante validación mandatoria por hito."
        },
        "content": {
          "activation": "Automatizada vía Hook nativo (delivery-discipline).",
          "rules": [
            {
              "name": "Reflejo de Disciplina",
              "details": "El sistema dispara automáticamente una alerta si se detectan más de 2 acciones técnicas (`write`, `replace`, `run`) sin una pausa de validación humana."
            },
            {
              "name": "Evidencia Obligatoria",
              "details": "Ante la alerta del sistema, el agente debe detenerse y presentar: 1) Captura textual, 2) Esquema de flujo, o 3) URL de servidor vivo."
            },
            {
              "name": "Pausa de Validación",
              "details": "Tras presentar la evidencia, el agente debe detenerse y solicitar explícitamente el feedback del usuario ('¿Se siente esto como lo esperas?')."
            },
            {
              "name": "Sincronización de Entorno",
              "details": "Antes de cualquier validación técnica, se debe verificar el estado del entorno (dependencias y migraciones) para evitar falsos positivos."
            }
          ],
          "prohibitions": [
            "Avanzar más de 2 hitos del Roadmap sin validación interactiva.",
            "Solicitar validación basada únicamente en descripciones narrativas ('Imagina que...')."
          ]
        },
        "status": "Activo",
        "related_components": ["PFS", "ROADMAP.md", "2025-12-31_ilusion_certeza_ejecucion.md"]
      }
    ]
  },
  "status": "Implementado",
  "related_components": ["PEG"]
}
