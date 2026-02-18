# Manifiesto de Portabilidad y Checklist de Desembarco (PDEL)
**ID:** ARC-PORT-001
**Versión:** 1.0
**Estado:** ACTIVO
**Fecha:** 2026-02-17

Este documento es la referencia autoritativa para el despliegue del Terroir de Holisto en entornos nuevos o desactualizados. Su propósito es garantizar la integridad de la **Triple Alianza** y la funcionalidad de la **Fisiología Nativa** (Hooks y Skills).

---

## 1. Requerimientos de Infraestructura
- [ ] **Node.js:** v18+ (necesario para `@google/gemini-cli`).
- [ ] **Python:** 3.10+ (necesario para el Exocórtex y Skills).
- [ ] **Git:** Configurado con credenciales para los repositorios del Terroir, Fenotipo y Semilla.

---

## 2. Checklist de Desembarco (Paso a Paso)

### Fase A: Sincronización de Código
1. [ ] **Orquestador:** `git pull origin master` en la raíz (`IA-HOLISTICA-1.0`).
2. [ ] **Fenotipo:** Clonar `PHENOTYPE` en la raíz (si no existe como submódulo activo).
3. [ ] **Semilla:** Clonar `Holisto_Seed` en `PROYECTOS/Evolucion_Terroir/` (si no existe).
4. [ ] **Verificación .gitignore:** Asegurar que `.gemini/` NO esté siendo ignorado localmente.

### Fase B: El Aliento del Sistema (.env)
1. [ ] **Restauración:** Copiar el archivo `.env` validado desde la bóveda de seguridad o dispositivo previo.
2. [ ] **Validación de Rutas:** Confirmar que las rutas son relativas (ej. `PHENOTYPE_ROOT=./PHENOTYPE`).
3. [ ] **Zona Horaria:** Ajustar `USER_TIMEZONE_OFFSET` si es necesario.

### Fase C: Metabolismo (Dependencias)
1. [ ] **Venv:** Crear/Activar entorno virtual (`python -m venv .venv`).
2. [ ] **Librerías:** `pip install -r requirements.txt`.
3. [ ] **Qdrant:** Asegurar conexión a Qdrant Cloud (validado automáticamente por `ingest.py` en PICS).

---

## 3. Validación de la Fisiología Nativa (Despertar)
Al iniciar el CLI, Holisto debe ejecutar el **PICS v6.9**. Verificar manualmente:

- [ ] **Reflejos (Hooks):** Ejecutar `/settings` y confirmar que el bloque `"hooks"` contiene el `traceability-reflex`.
- [ ] **Órganos (Skills):** Ejecutar `/skills list` y confirmar la presencia de:
    - `agenda-management`
    - `session-harvesting`
    - `memory-hygiene`
- [ ] **Memoria Forense:** Verificar que `PHENOTYPE/SYSTEM/MEMORIA/logs_vigia/ARCHIVE` es accesible.

---

## 4. Notas de Contingencia
* Si el CLI no reconoce los hooks, forzar la escritura de `.gemini/settings.json` desde una sesión activa.
* Si el `traceability-reflex` falla, verificar que la ruta al script en el hook sea correcta para el OS actual (win32).

---
*Este documento debe ser consultado obligatoriamente por el agente en situaciones de migración o fallos de coherencia post-mudanza.*
