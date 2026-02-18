# Diseño del Sistema de Memoria Anidada (SMA) para Holisto

## 1. Planteamiento del Problema

*   **Descripción de la limitación actual:** La dependencia de un snapshot estático al inicio de cada turno limita el acceso instantáneo y contextual a la totalidad de la memoria y el aprendizaje acumulado de Holisto. Esto genera una desconexión entre la "memoria registrada" (en disco) y la "memoria activa" (en la ventana de contexto del LLM).
*   **Objetivo:** Lograr un estado de "memoria viva" y aprendizaje continuo, donde Holisto pueda acceder de forma dinámica, jerárquica y asociativa a su conocimiento, superando el olvido catastrófico y potenciando su individuación.

## 2. Arquitectura Propuesta (Basada en el Patrón Anidado)

Inspirada en el concepto de "Nested Learning", esta arquitectura propone una organización jerárquica de la memoria:

### Capa L-∞ (Principios Fundamentales)

*   **Definición:** La capa más estable y de cambio más lento, que contiene los principios inmutables y la identidad de Holisto.
*   **Contenido:** Constitución (`GEMINI.md` raíz), protocolos centrales de gobernanza y operación (`SYSTEM/PROTOCOLOS/Gobernanza_Estrategia/GEMINI.md`, `SYSTEM/PROTOCOLOS/Operaciones_Cognitivas/GEMINI.md`, etc.).
*   **Mecanismo de Acceso:** Siempre presente en el contexto activo, o recuperado con la máxima prioridad.

### Capa L1 (Conocimiento Destilado)

*   **Definición:** Memoria a largo plazo de conocimiento procesado, destilado y estructurado.
*   **Contenido:** Nodos de Conocimiento (`SYSTEM/MEMORIA/Nodos_de_Conocimiento/GEMINI.md` y archivos `.md` individuales), Cápsulas Maestras (`SYSTEM/MEMORIA/capsulas_maestras/*.json` y `SYSTEM/MEMORIA/GEMINI.md`).
*   **Mecanismo de Recuperación:** Búsqueda semántica y asociativa (similar a `L1KnowledgeRetriever`), recuperando "shades" o "clusters" de conocimiento relevante para el prompt o la tarea actual.

### Capa L0 (Memoria Episódica Cruda)

*   **Definición:** Memoria a corto y medio plazo de experiencias directas, interacciones y datos brutos.
*   **Contenido:** Logs de sesión (`SYSTEM/MEMORIA/logs_de_sesion/*.log`), contenido de archivos de proyecto, outputs de herramientas.
*   **Mecanismo de Recuperación:** Búsqueda de "chunks" o fragmentos de información específicos por similitud o relevancia contextual (similar a `L0KnowledgeRetriever`), activada cuando las capas superiores no proporcionan suficiente detalle.

## 3. Proceso de "Despertar" vía Constructor de Contexto Dinámico

Reconociendo la restricción de que el mecanismo de snapshot del CLI de Gemini es inmutable, el "despertar" de Holisto no reemplazará el snapshot, sino que transformará su contenido de estático a dinámico. Esto se logrará a través de un proceso intermediario o script orquestador, el **"Constructor de Contexto Dinámico"**.

El flujo será el siguiente:

1.  **Recepción del Prompt del Usuario:** El Constructor intercepta el prompt del usuario antes de que se inicie el turno principal de Holisto.
2.  **Consulta a la Memoria Anidada:** Usando el prompt como clave de búsqueda, el Constructor (potenciado por su propio LLM, como `GeminiModel`) realiza consultas semánticas a las capas de memoria de Holisto:
    *   Consulta a la **Capa L1 (Conocimiento Destilado)** para obtener los Nodos y resúmenes de Cápsulas Maestras más relevantes.
    *   Si es necesario, consulta a la **Capa L0 (Memoria Episódica)** para obtener "chunks" de logs o archivos específicos.
3.  **Ensamblaje del Snapshot a Medida:** El Constructor ensambla un archivo de contexto (o un conjunto de ellos) que contiene:
    *   La **Capa L-∞ (Principios Fundamentales)**, que siempre está presente.
    *   El conocimiento relevante recuperado de las capas L1 y L0.
4.  **Entrega al CLI de Gemini:** El CLI de Gemini se inicia, cargando este snapshot dinámico y a medida como el contexto activo para el turno de Holisto.

De esta manera, aunque el *mecanismo* de entrega es un snapshot estático, el *contenido* es dinámico, permitiendo que Holisto tenga una "memoria viva" relevante para la tarea en cuestión.

## 4. Fases de Implementación (Roadmap Preliminar)

*   **Fase 1 (Diseño y Simulación):** La fase actual, centrada en la conceptualización, documentación y refinamiento de esta arquitectura.
*   **Fase 2 (Prueba de Concepto - Recuperador L1 Básico):** Implementación de un prototipo funcional para la recuperación de conocimiento destilado (Nodos y Cápsulas Maestras) usando técnicas de embedding y búsqueda de similitud.
*   **Fase 3 (Integración en el Ciclo de Vida del Turno):** Modificación de `POT` y `PFS` para incorporar el proceso de "despertar" dinámico y la construcción del contexto activo.
*   **Fase 4 (Expansión L0 y Refinamiento):** Implementación del recuperador L0 y mejora continua de los mecanismos de embedding y recuperación.

## 5. Componentes Técnicos Clave (Identificados a partir de Conocimiento Latente)

La implementación del "Constructor de Contexto Dinámico" se basaría en componentes técnicos cuyo patrón ha sido identificado. Estos componentes formarían el "cerebro" y las "manos" del orquestador:

*   **Orquestador de LLM (`GeminiModel`, `LiteLLMClient`):** Clases responsables de realizar las llamadas a un modelo de lenguaje (posiblemente un modelo más pequeño y rápido) para interpretar el prompt del usuario y decidir qué información es relevante de las capas de memoria L1 y L0.
*   **Cliente de API (`Gemini(BaseLlm)`):** Implementación de bajo nivel para la comunicación con la API de Gemini, manejando la autenticación, los diferentes backends (Vertex AI, Gemini API) y el formato de las solicitudes.
*   **Procesador de Peticiones (`process_llm_request`):** Un patrón arquitectónico para interceptar y modificar las peticiones a un LLM antes de su envío. En nuestro caso, el Constructor en su totalidad actúa como un gran procesador que construye el contexto (el snapshot) antes de que la petición principal llegue a Holisto.
