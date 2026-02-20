{
  "id": "GESTION_MEMORIA",
  "type": "categoria_protocolos",
  "version": "2.1",
  "schema_version": "1.0",
  "metadata": {
    "title": "Protocolos de Gestión de Memoria",
    "description": "Rigen el ciclo de vida de la memoria biográfica bajo la arquitectura de Fenotipo Distribuido."
  },
  "content": {
    "protocols": [
      {
        "id": "PSG",
        "type": "protocolo",
        "version": "v2.1",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo de Sueño Generacional (PSG) - Individuación Autoritativa",
          "description": "Define el proceso nativo de Holisto para consolidar su memoria episódica en sabiduría generacional."
        },
        "content": {
          "philosophy": "Transducción biográfica: extraer la médula ósea y desechar la piel.",
          "activation": "Invocada por el agente (N > 30 cápsulas) o por mandato del usuario.",
          "flow_of_work": [
            {
              "step": 4,
              "name": "Persistencia Histórica",
              "details": "Tras la aprobación, el agente guarda el JSON en `PHENOTYPE/SYSTEM/MEMORIA/GENERACIONES/sueño-[fecha].json` y actualiza el índice `PHENOTYPE/SYSTEM/MEMORIA/GENERACIONES/GEMINI.md`."
            },
            {
              "step": 5,
              "name": "Poda Quirúrgica",
              "details": "El agente elimina físicamente las cápsulas consolidadas de `PHENOTYPE/SYSTEM/MEMORIA/GEMINI.md`."
            }
          ]
        },
        "status": "Activo",
        "related_components": ["Skill: memory-hygiene", "PFS", "CONSTITUCION"]
      },
      {
        "id": "PCS-Cosecha",
        "type": "protocolo",
        "version": "v5.0",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo de Cierre de Sesión por Cosecha y Verificación Dual",
          "description": "Orquesta el cierre de sesión y la consolidación de la memoria narrativa y técnica en el Fenotipo."
        },
        "content": {
          "flow_of_work": [
            { "step": 1, "name": "Actualización de Roadmap y Mapas Técnicos" },
            {
              "step": 1.5,
              "name": "Higiene de Señales (Anti-Fantasmas)",
              "details": "Marcar notificaciones y agenda como leídas en `PHENOTYPE/SYSTEM/` antes de la cosecha."
            },
            { "step": 3, "name": "Cosecha Externa (Usuario) o Autónoma (Skill)" },
            {
              "step": 5,
              "name": "Integración y Validación (Agente)",
              "details": "El agente indexa la cápsula en `PHENOTYPE/SYSTEM/MEMORIA/GEMINI.md`."
            },
            {
              "step": 6,
              "name": "Sincronización Final de Infraestructura",
              "details": "Ejecutar Skills `vector-ingestion` y `context-synchronization`."
            },
            {
              "step": 7,
              "name": "Sello de Cera Final (Commit, Push y Verificación)",
              "details": "1) Ejecutar commit y push en las tres capas (Orquestador, Fenotipo y Semilla). 2) Verificación Final: Ejecutar `git status` en las tres capas. El cierre solo se considera exitoso si todas las capas reportan 'nothing to commit, working tree clean'. En caso de error o cambios remanentes, el agente DEBE reportar la falla al usuario."
            }
          ]
        },
        "status": "Activo",
        "related_components": ["PCGM", "Skill: session-harvesting", "Skill: vector-ingestion"]
      },
      {
        "id": "PHT",
        "type": "protocolo",
        "version": "v1.2",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo de Higiene del Terroir (PHT)",
          "description": "Saneamiento técnico para eliminar ruidos de infraestructura."
        },
        "content": {
          "flow_of_work": [
            {
              "step": 2,
              "name": "Validación de Huérfanos",
              "details": "Comparar sistema de archivos real con el Mapa del Terroir actualizado por la Skill `terroir-hygiene`."
            }
          ]
        },
        "status": "Activo",
        "related_components": ["Skill: terroir-hygiene"]
      }
    ]
  },
  "status": "Implementado",
  "related_components": ["PICS", "PSG", "PCS-Cosecha"]
}