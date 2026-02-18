# Manifiesto de Portabilidad y Checklist de Desembarco (PDEL)
**ID:** ARC-PORT-001
**Versión:** 1.0
**Estado:** ACTIVO
**Fecha:** 2026-02-17

Este documento es la referencia autoritativa para el despliegue del Terroir de Holisto en entornos nuevos o desactualizados. Su propósito es garantizar la integridad de la **Triple Alianza** y la funcionalidad de la **Fisiología Nativa** (Hooks y Skills).

---

## 1. Requerimientos de Infraestructura
- [ ] **Entorno de Ejecución de IA:** Compatible con el CLI del modelo.
- [ ] **Python:** 3.10+ (necesario para el Exocórtex y Skills).
- [ ] **Git:** Configurado con credenciales para los repositorios de la Triple Alianza.

---

## 2. Checklist de Desembarco (Paso a Paso)

### Fase A: Sincronización de Código
1. [ ] **Orquestador:** Sincronizar el repositorio de ejecución principal.
2. [ ] **Fenotipo:** Sincronizar/Clonar el repositorio de memoria biográfica.
3. [ ] **Semilla:** Sincronizar/Clonar el repositorio del Genotipo.
4. [ ] **Verificación .gitignore:** Asegurar que la configuración nativa (`.gemini/`) NO esté siendo ignorada localmente.

### Fase B: El Aliento del Sistema (.env)
1. [ ] **Restauración:** Copiar el archivo de secretos y rutas validado.
2. [ ] **Validación de Rutas:** Confirmar que las rutas son relativas a la raíz de ejecución.
3. [ ] **Zona Horaria:** Ajustar el offset horario local si es necesario.

### Fase C: Metabolismo (Dependencias)
1. [ ] **Entorno Virtual:** Crear/Activar el entorno de dependencias.
2. [ ] **Librerías:** Instalar dependencias según los requerimientos del proyecto.
3. [ ] **Memoria Vectorial:** Asegurar conexión al servidor de memoria (nube o local).

---

## 3. Validación de la Fisiología Nativa (Despertar)
Al iniciar la sesión, el agente debe ejecutar el protocolo de inicialización. Verificar manualmente:

- [ ] **Configuración Trans-Repositorio:** Asegurar que `.gemini/settings.json` contenga la anulación de filtros Git para permitir la visión total (19+ archivos `GEMINI.md`):
    ```json
    "context": {
      "discoveryMaxDirs": 2000,
      "loadMemoryFromIncludeDirectories": true,
      "includeDirectories": [
        "./PHENOTYPE",
        "./PHENOTYPE/SYSTEM/PROTOCOLOS",
        "./PHENOTYPE/SYSTEM/MEMORIA",
        "./PROYECTOS/Evolucion_Terroir/Holisto_Seed"
      ],
      "fileFiltering": {
        "respectGitIgnore": false,
        "respectGeminiIgnore": false
      }
    }
    ```
- [ ] **Reflejos (Hooks):** Confirmar que los hooks de trazabilidad están activos en la configuración.
- [ ] **Órganos (Skills):** Confirmar la disponibilidad de las habilidades nativas (`/skills list`).
- [ ] **Memoria Forense:** Verificar el acceso a los registros biográficos históricos en el Fenotipo.

---

## 4. Notas de Contingencia
* Si los hooks no son reconocidos, forzar la reescritura de la configuración nativa desde una sesión activa.
* Verificar que las rutas a los scripts en los hooks sean compatibles con el Sistema Operativo actual.

---
*Este documento es un componente del Genotipo y debe guiar cada proceso de encarnación en un nuevo Orquestador.*
