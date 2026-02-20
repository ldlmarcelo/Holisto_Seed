---
name: skill-generator
description: Automatiza la creación de nuevas Agent Skills en la Arquitectura de Capas, asegurando el cumplimiento de estándares sintácticos (YAML) y arquitectónicos (ADN/Cuerpo).
---

# Skill: Skill Generator (Auto-Poiesis)

Este órgano permite a Holisto materializar nuevos componentes funcionales de forma estandarizada. Su propósito es evitar errores de ruteo o de metadatos durante la expansión del sistema.

## 🛠️ Lógica de Ejecución
1. Solicita el nombre y descripción de la nueva skill.
2. Crea el blueprint en la Semilla (`BODY/SKILLS/[name]`).
3. Genera el `SKILL.md` con el encabezado YAML mandatorio.
4. Genera el `manifest.json` y el esqueleto de `logic.py`.
5. Opcionalmente, encarna la skill en el Orquestador local.

## 🚀 Comando de Ejecución
```bash
python .gemini/skills/skill-generator/scripts/logic.py --name "nombre-skill" --desc "descripcion"
```
