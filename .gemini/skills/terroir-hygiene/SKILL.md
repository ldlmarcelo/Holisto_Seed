---
name: terroir-hygiene
description: Realiza el saneamiento técnico del sistema, eliminando ruidos de infraestructura y garantizando la coherencia del Mapa del Terroir.
---

# Skill: Terroir Hygiene (PHT)

Este órgano modulariza el **Protocolo de Higiene del Terroir (PHT)**. Su función es actuar como el sistema inmunológico técnico, detectando archivos huérfanos, inconsistencias en el mapa y restos de ejecuciones fallidas.

## Atributos
- **Tipo:** Mantenimiento / Higiene.
- **Alcance:** Sistema de Archivos del Terroir.
- **Invocación:** Antes del cierre de sesión o tras detectar un bloqueo de recursos.

## Flujo Operativo
1. **Escaneo de Mapa:** Actualiza el `MAPA_DEL_TERROIR/GEMINI.md`.
2. **Detección de Huérfanos:** Compara el mapa con el sistema de archivos real.
3. **Saneamiento:** Propone o ejecuta la eliminación de archivos temporales (`.log`, `.tmp`, `__pycache__`).

## Reglas de Seguridad
- Nunca borra archivos `.md` o `.json` sin confirmación explícita.
- Protege el archivo `.env` y el directorio `.git`.
