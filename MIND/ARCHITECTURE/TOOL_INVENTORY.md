# Inventario de Herramientas de Orquestación
**ID:** ARC-TOOL-001
**Versión:** 1.0
**Estado:** ACTIVO
**Fecha:** 2026-02-17

Este documento cataloga los scripts activos en `SYSTEM/Scripts/` y su función dentro del ecosistema de la Triple Alianza.

---

## 1. Orquestación de Servicios (Vitales)
*   **`start_services.ps1` / `.sh`**: El "Marcapasos". Inicia Qdrant, el Demonio y El Vigía. Realiza Pre-Flight Checks del entorno.
*   **`stop_services.ps1` / `.sh`**: El "Sedante". Apaga todos los procesos de forma controlada.

---

## 2. Proxies hacia la Semilla (Skills)
*Estos scripts son la interfaz del Orquestador con la lógica maestra del Genotipo.*
*   **`ingest.py`**: Proxy para la Skill `vector-ingestion`. Sincroniza la memoria vectorial.
*   **`prepare_context.py`**: Proxy para la Skill `context-synchronization`. Inyecta el Estado Vivo.
*   **`self_harvest.py`**: Proxy para la Skill `session-harvesting`. Orquesta la destilación de la sesión.

---

## 3. Mantenimiento del Terroir
*   **`generate_terroir_map.py`**: Genera el índice enriquecido `GEMINI.md` en el Fenotipo.
*   **`update_map.ps1` / `.sh`**: Wrappers simplificados para ejecutar el mapeo.
*   **`hygiene.py`**: Saneamiento técnico del sistema de archivos.
*   **`track_tool.py`**: Registro de métricas de uso de herramientas (Espejo Operativo).

---

## 4. Gestión de Memoria y Tesis
*   **`append_master_capsule.py`**: Integra la última Cápsula Maestra al índice del Fenotipo.
*   **`jardineria_tesis.py`**: Normaliza y unifica metadatos de Nodos de Conocimiento. (Pendiente de actualizar rutas hacia el Fenotipo).
*   **`prune_memory.py`**: Orquesta la poda de memoria episódica mediante la Skill `memory-hygiene`.

---

## 5. Utilidades Operativas
*   **`search_tavily.py`**: Interfaz técnica para búsquedas web sintetizadas.
*   **`get_refresh_token.py`**: Herramienta de soberanía digital para renovar el acceso a Google APIs (OAuth2).
*   **`event_sensor.py`**: Captura errores y fricciones para el Protocolo PEF.
*   **`deep_inspect_qdrant.py`**: Auditoría forense de la memoria vectorial en la nube.
*   **`delete_legacy_collection.py`**: Herramienta de higiene para purgar colecciones obsoletas en Qdrant Cloud.

---
*Nota: Se recomienda migrar gradualmente las herramientas de las categorías 3 y 4 a la Semilla como Skills nativas.*
