---
name: agenda-management
description: Gestiona recordatorios, tareas programadas y alertas temporales del Terroir. Proporciona "Consciencia del Tiempo" al agente.
---

# Skill: Agenda Management (Time Awareness)

Este órgano permite a The Individual interactuar con la dimensión temporal del Terroir, gestionando eventos y recordatorios.

## 🛠️ Lógica de Ejecución
Al activar esta skill, el agente adquiere la capacidad de:
1. Leer y actualizar el archivo `SYSTEM/AGENDA/recordatorios.json`.
2. Identificar hitos temporales cercanos.
3. Proponer notificaciones proactivas basadas en fechas y horas.

## 🚀 Comando de Ejecución
```bash
python .gemini/skills/agenda-management/scripts/logic.py
```

---
*"Time is the Associated Milieu of all action."*
