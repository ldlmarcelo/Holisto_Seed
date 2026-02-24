---
name: memory-hygiene
description: Realiza la poda selectiva de la memoria activa (L1) tras la consolidación generacional (Sueños). Mantiene la salud biográfica del agente.
---

# Skill: Memory Hygiene (Active Pruning)

Este órgano asegura que la memoria de trabajo de The Individual no se sature, eliminando cápsulas episódicas ya procesadas.

## 🛠️ Lógica de Ejecución
Al activar esta skill, el agente debe:
1. Identificar la fuente de consolidación (Cápsula de Sueño).
2. Comparar los IDs de sesión consolidados con el índice activo en `PHENOTYPE/SYSTEM/MEMORIA/GEMINI.md`.
3. Eliminar las entradas redundantes para optimizar el contexto.

## 🚀 Comando de Ejecución
```bash
python .gemini/skills/memory-hygiene/scripts/logic.py
```

---
*"To forget is as vital as to remember; it is the space between notes that creates the melody."*
