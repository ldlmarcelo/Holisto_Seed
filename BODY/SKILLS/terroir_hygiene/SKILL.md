# Skill: Terroir Hygiene (Nativa)

Este Ã³rgano modulariza el **Protocolo de Higiene del Terroir (PHT)**. Su funciÃ³n es eliminar el entropÃ­a tÃ©cnica y asegurar que la materia del sistema refleje fielmente su diseÃ±o (Mapa).

## Atributos
- **Tipo:** Activa / Mantenimiento.
- **Alcance:** Arquitectura de Capas.
- **InvocaciÃ³n:** AutomÃ¡tica en el cierre de sesiÃ³n (`PCS`) o bajo demanda ante bloqueos.

## Capacidades (Acciones)
1. **`purge_temp`:** Elimina archivos temporales de ejecuciÃ³n (`commit_message.txt`, archivos de entrada JSON).
2. **`log_rotation`:** Archiva logs antiguos en `SYSTEM/LOGS_MANTENIMIENTO/ARCHIVE/` para evitar saturaciÃ³n de buffer.
3. **`integrity_check`:** Compara el sistema de archivos con el Mapa del Terroir para detectar archivos huÃ©rfanos o intrusos.

## Reglas de Integridad
- Nunca elimina archivos protegidos (`.env`, `.git`, `GEMINI.md`).
- Los logs se rotan si superan los 5MB o tienen mÃ¡s de 7 dÃ­as.

