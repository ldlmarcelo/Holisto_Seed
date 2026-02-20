# Skill: Project Management (Nativa)

Este órgano modulariza el **Sistema de Gestión de Proyectos (SGP)**. Su función es centralizar el ciclo de vida de los proyectos, desde su gÃ©nesis hasta su activaciÃ³n cognitiva.

## Atributos
- **Tipo:** Activa / Orquestadora.
- **Alcance:** Orquestador (RaÃ­z).
- **InvocaciÃ³n:** Cuando el agente o el usuario necesitan interactuar con la estructura de proyectos del Terroir.

## Capacidades (Acciones)
1. **`list`:** Muestra un resumen de todos los proyectos registrados y su estado.
2. **`activate`:** Carga el contexto de un proyecto (README, ROADMAP, ARCHITECTURE) en la memoria de trabajo.
3. **`create`:** Genera la estructura de un nuevo proyecto e indexa su metadata en `PROYECTOS/GEMINI.md`.

## Reglas de Integridad
- Todo proyecto debe tener un ID Ãºnico.
- La activaciÃ³n de un proyecto actualiza el campo `last_activated` en el Ã­ndice central.
- Los directorios de categorÃ­as se respetan estrictamente (`dev`, `ped`, `research`, `terroir-evo`).
