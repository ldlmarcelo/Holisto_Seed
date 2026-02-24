# Skill: vision-control

Esta habilidad permite gestionar la ventana de contexto del agente, silenciando archivos `GEMINI.md` no vitales para reducir el ruido y el consumo de tokens, manteniendo una red de seguridad (Botón de Pánico).

## Modos de Operación

1.  **Enfoque (`--focus`):** Renombra archivos `GEMINI.md` irrelevantes a `MUTE_GEMINI.md`.
2.  **Pánico (`--panic`):** Restaura todos los archivos a `GEMINI.md` para recuperar la visión total.

## Médula Ósea (Archivos Protegidos)
Los siguientes archivos nunca se silencian:
*   Constitución (Raíz)
*   Mapa del Terroir
*   Perfil de Usuario
*   Índice de Proyectos
*   Mapa de Arquitectura
*   Índice de Memoria
*   Índice de Sabiduría

## Uso Técnico
Invoke via PowerShell:
`.\.venv\Scripts\python.exe .gemini/skills/vision-control/scripts/logic.py --focus`
`.\.venv\Scripts\python.exe .gemini/skills/vision-control/scripts/logic.py --panic`
