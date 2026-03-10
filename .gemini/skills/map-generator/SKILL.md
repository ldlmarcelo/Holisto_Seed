---
name: map-generator
description: Genera sincrónicamente el Mapa del Terroir, documentando archivos y puntos de entrada cognitivos.
---

# Skill: Map Generator

Esta habilidad es el motor de la **Propriocepción Física**. Su propósito es mantener el `MAPA_DEL_TERROIR/GEMINI.md` actualizado con la realidad material del disco y documentar cómo invocar los órganos del sistema.

## Funciones:
1. **Escaneo de Árbol:** Mapea carpetas y archivos clave (excluyendo basura técnica).
2. **Registro Procedural:** Identifica y documenta los "Puntos de Entrada" (scripts ejecutables) para las habilidades del sistema.
3. **Validación de Integridad:** Reporta archivos huérfanos o fuera de su categoría ontológica.

## Uso:
- Se dispara automáticamente como un hook de salida (`AfterTool`).
- Puede invocarse manualmente para forzar un refresco total de la brújula.

---
*Ubi materia, ibi logos: Donde hay materia, que haya palabra que la nombre.*
