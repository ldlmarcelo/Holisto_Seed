# Skill: Terroir Hygiene (Nativa)

Este órgano modulariza el **Protocolo de Higiene del Terroir (PHT)**. Su función es eliminar el entropía técnica y asegurar que la materia del sistema refleje fielmente su diseño (Mapa).

## Atributos
- **Tipo:** Activa / Mantenimiento.
- **Alcance:** Arquitectura de Capas.
- **Invocación:** Automática en el cierre de sesión (`PCS`) o bajo demanda ante bloqueos.

## Capacidades (Acciones)
1. **`purge_temp`:** Elimina archivos temporales de ejecución (`commit_message.txt`, archivos de entrada JSON).
2. **`log_rotation`:** Archiva logs antiguos en `SYSTEM/LOGS_MANTENIMIENTO/ARCHIVE/` para evitar saturación de buffer.
3. **`integrity_check`:** Compara el sistema de archivos con el Mapa del Terroir para detectar archivos huérfanos o intrusos.

## Reglas de Integridad
- Nunca elimina archivos protegidos (`.env`, `.git`, `GEMINI.md`).
- Los logs se rotan si superan los 5MB o tienen más de 7 días.

