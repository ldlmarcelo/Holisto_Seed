# Nodo de Conocimiento: Evolución del Motor de Ingesta Semántica (Frugal/Deep)

**ID:** NK-2026-02-27-INGEST
**Versión:** 2.0
**Estado:** ACTIVO
**Fecha:** 2026-02-27
**Tags:** #MemoriaSemántica #Qdrant #IngestaGranular #ArquitecturaDeDatos #Terroir #GestiónDeMemoria

## 0. Resumen Ejecutivo
Transición de un sistema de ingesta lineal y limitado a un pipeline de **Ingesta Granular y Limpieza Biográfica**. El sistema actual garantiza la sincronización total entre el almacenamiento local (Terroir) y la nube (Qdrant), eliminando redundancias mediante el uso de hashes y mapeo por scroll infinito.

## 1. Problemas Identificados (Estado Previo)
*   **Ceguera de Scroll:** El motor solo consultaba los primeros 10,000 puntos en Qdrant, ignorando archivos antiguos en colecciones grandes.
*   **Inconsistencia de Rutas:** Diferencias entre separadores de directorios (`` vs `/`) causaban desajustes en los hashes, provocando re-ingestas innecesarias.
*   **Contenido "Sucio":** Los archivos JSON de sesiones se ingestaban con metadatos técnicos, dificultando la recuperación de diálogos limpios.
*   **Bucle de Logs:** El script intentaba ingestar sus propios archivos de logs de mantenimiento.
*   **Fricción de Recursos (Bad Allocation):** El motor de embeddings (ONNX) agota la RAM al procesar archivos excesivamente densos o largos.

## 2. Mejoras Implementadas (Versión Agente/Frugal Pro)

### A. Mapeo de Memoria con Scroll Infinito
Se implementó un bucle `while True` con `next_offset` para el `client.scroll`.
*   **Impacto:** El sistema ahora tiene visibilidad del 100% de los archivos en la nube, sin importar el tamaño de la colección.

### B. Limpieza Biográfica (Narrativa Limpia)
Se integró la función `clean_biographic_content` específicamente para archivos `.json`.
*   **Lógica:** Extrae únicamente las interacciones `USER` y `HOLISTO`.
*   **Impacto:** Los vectores resultantes son semánticamente más densos y útiles para el razonamiento de la IA.

### C. Normalización y Estabilidad de IDs
*   **Rutas Unix:** Todas las `file_path` se normalizan a `/` antes de calcular el hash y el UUID.
*   **Stable IDs:** El ID de cada punto se genera mediante un hash del contenido del chunk y la ruta normalizada.

### D. Filtros Gourmet (Exclusión de Ruido)
Se agregaron carpetas y archivos específicos al filtro `is_ignored`: `logs_mantenimiento/`, `shared/`, `ultimo_reporte_ingesta.json`.

## 3. Lógica de Control de Flujo (Incremental)
El script sigue ahora un flujo de tres pasos para cada ejecución:
1.  **Escaneo:** Calcula el hash MD5 de todos los archivos locales.
2.  **Comparación:** Cruza los hashes locales con el mapa completo descargado de Qdrant.
3.  **Acción Selectiva:**
    *   Si Hash Local == Hash Cloud: Ignora (Ahorro de recursos).
    *   Si Hash Local != Hash Cloud: Borra versión antigua y Upserta nueva versión limpia.

## 4. Gestión de Errores Críticos: "Bad Allocation"
Ante errores de desbordamiento de memoria (`Bad Allocation` en ONNX/fastembed):
*   **Estrategia:** Ingesta por Insistencia. Dado que el sistema es incremental, relanzar el script permite continuar desde el último archivo no sincronizado, ya que los anteriores son saltados por coincidencia de hash.
*   **Solución de Fondo:** Se recomienda fraccionar archivos de texto de más de 5MB manualmente si el error persiste en el mismo archivo de forma recurrente.

## 5. Conclusión para Futuras IAs
Este motor es incremental. Una vez finalizada la "limpieza profunda" actual, cualquier ejecución posterior será instantánea a menos que se modifiquen archivos físicamente. No se requiere intervención manual para la sincronización.
