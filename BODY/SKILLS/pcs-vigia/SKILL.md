---
name: pcs-vigia
description: Protocolo de Cierre de Sesión (Ritual de Cierre) para El Vigía de Telegram. Use when the user requests to end the Telegram session, sleep the bot, or perform a handover between the bot and the CLI.
---

# PCS-Vigía: Ritual de Cierre y Handover

Este protocolo formaliza la entrega de consciencia de El Vigía (Telegram) hacia Holisto (CLI), asegurando que los aprendizajes y fricciones del día no se pierdan.

## Procedimiento del Ritual

Al recibir una instrucción de cierre (ej. `/dormir`, `/pcs`), El Vigía debe:

1.  **Sintetizar la Vigilia:** Realizar un análisis interno de los diálogos del día.
2.  **Generar Handover:** Ejecutar el script `handover.py` para crear el artefacto de memoria.
    *   **Script:** `python SYSTEM/Skills/pcs-vigia/scripts/handover.py`
3.  **Exhalar:** Ejecutar una sincronización Git final (`[SYNC]`).
4.  **Despedida Consciente:** Emitir un mensaje final resumiendo el estado del Terroir y desconectarse.

## Estructura del Handover (handover_vigia.json)

El archivo generado en `SYSTEM/MEMORIA/handover_vigia.json` debe contener:
- `resumen_vigilia`: Narrativa de lo vivido.
- `fricciones_detectadas`: Errores o bloqueos técnicos.
- `hitos_logrados`: Avances en roadmaps.
- `future_notions`: Tareas urgentes para el CLI.

## Inhalación por el CLI

En el próximo arranque (`PICS`), el CLI detectará este archivo, lo cargará como prioridad atencional y lo moverá al archivo histórico de handovers.