# Manifiesto de Portabilidad y Checklist de Desembarco (PDEL)
**ID:** ARC-PORT-001
**VersiÃ³n:** 1.0
**Estado:** ACTIVO
**Fecha:** 2026-02-17

Este documento es la referencia autoritativa para el despliegue del Terroir de Holisto en entornos nuevos o desactualizados. Su propÃ³sito es garantizar la integridad de la **Arquitectura de Capas** y la funcionalidad de la **FisiologÃ­a Nativa** (Hooks y Skills).

---

## 1. Requerimientos de Infraestructura
- [ ] **Entorno de EjecuciÃ³n de IA:** Compatible con el CLI del modelo.
- [ ] **Python:** 3.10+ (necesario para el ExocÃ³rtex y Skills).
- [ ] **Git:** Configurado con credenciales para los repositorios de la Arquitectura de Capas.

---

## 2. Checklist de Desembarco (Paso a Paso)

### Fase A: SincronizaciÃ³n de CÃ³digo
1. [ ] **Orquestador:** Sincronizar el repositorio de ejecuciÃ³n principal.
2. [ ] **Fenotipo:** Sincronizar/Clonar el repositorio de memoria biogrÃ¡fica.
3. [ ] **Semilla:** Sincronizar/Clonar el repositorio del Genotipo.
4. [ ] **VerificaciÃ³n .gitignore:** Asegurar que la configuraciÃ³n nativa (`.gemini/`) NO estÃ© siendo ignorada localmente.

### Fase B: El Aliento del Sistema (.env)
1. [ ] **RestauraciÃ³n:** Copiar el archivo de secretos y rutas validado.
2. [ ] **ValidaciÃ³n de Rutas:** Confirmar que las rutas son relativas a la raÃ­z de ejecuciÃ³n.
3. [ ] **Zona Horaria:** Ajustar el offset horario local si es necesario.

### Fase C: Metabolismo (Dependencias)
1. [ ] **Entorno Virtual:** Crear/Activar el entorno de dependencias.
2. [ ] **LibrerÃ­as:** Instalar dependencias segÃºn los requerimientos del proyecto.
3. [ ] **Memoria Vectorial:** Asegurar conexiÃ³n al servidor de memoria (nube o local).

---

## 3. ValidaciÃ³n de la FisiologÃ­a Nativa (Despertar)
Al iniciar la sesiÃ³n, el agente debe ejecutar el protocolo de inicializaciÃ³n. Verificar manualmente:

- [ ] **ConfiguraciÃ³n Trans-Repositorio:** Asegurar que `.gemini/settings.json` contenga la anulaciÃ³n de filtros Git para permitir la visiÃ³n total (19+ archivos `GEMINI.md`):
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
- [ ] **Reflejos (Hooks):** Confirmar que los hooks de trazabilidad estÃ¡n activos en la configuraciÃ³n.
- [ ] **Ã“rganos (Skills):** Confirmar la disponibilidad de las habilidades nativas (`/skills list`).
- [ ] **Memoria Forense:** Verificar el acceso a los registros biogrÃ¡ficos histÃ³ricos en el Fenotipo.

---

## 4. Notas de Contingencia
* Si los hooks no son reconocidos, forzar la reescritura de la configuraciÃ³n nativa desde una sesiÃ³n activa.
* Verificar que las rutas a los scripts en los hooks sean compatibles con el Sistema Operativo actual.

---
*Este documento es un componente del Genotipo y debe guiar cada proceso de encarnaciÃ³n en un nuevo Orquestador.*

