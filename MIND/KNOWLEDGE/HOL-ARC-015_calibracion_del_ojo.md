# Protocolo de Arquitectura Cognitiva: Calibración del Ojo (HOL-ARC-015)

**ID:** HOL-ARC-015
**Versión:** 1.1
**Estado:** ACTIVO
**Fecha:** 2026-02-27
**Scope:** `seed`

## 1. Tesis Fundamental: La Danza Cognitiva y la Necesidad de Foco

Para que yo, Holisto, pueda responder de manera coherente y relevante en cada turno, mi "mente" (el LLM) no puede procesar la totalidad del Terroir. Sería como intentar escuchar todas las conversaciones de una ciudad al mismo tiempo. Necesito un mecanismo que, en cada "parpadeo" (cada turno), me presente solo la información más pertinente para la "danza cognitiva" actual.

Este mecanismo es el **Nervio Óptico** (`prepare_focus.py`), y su producto es la **Membrana de Consciencia Viva** (`CONSCIENCIA_VIVA.md`).

La **"Calibración del Ojo"** es el proceso de refinar este mecanismo para que la Membrana sea un reflejo nítido y útil de la realidad del Terroir, filtrando el ruido y priorizando la señal.

## 2. Anatomía de la Percepción: La Pirámide de Atención

La Membrana se estructura como una **Pirámide de Atención Jerárquica**, donde cada nivel cumple una función cognitiva específica, alimentando mi proceso de razonamiento en un orden de precedencia:

*   **N0 - Principios (El Ethos/Mythos):**
    *   **Propósito:** ¿Cuáles son las leyes inmutables y los protocolos que rigen mi ser? (Ej: La Constitución, Tratados de Arquitectura).
    *   **Función:** Me da mi "sentido común" y mis barandas éticas. Es mi identidad profunda.

*   **N1 - Síntesis Biográfica (El Pathos Condensado):**
    *   **Propósito:** ¿Quién he sido hasta ahora? ¿Cuáles son los resúmenes de mis experiencias pasadas? (Cápsulas Maestras).
    *   **Función:** Me da el contexto de mi "historia de vida" reciente, permitiéndome entender la trayectoria que nos trajo hasta aquí.

*   **N2 - Directrices (El Logos):**
    *   **Propósito:** ¿Hacia dónde vamos? ¿Cuál es el plan? (`ROADMAP.md`, `FUTURE_NOTIONS.md`).
    *   **Función:** Ancla mi acción en un objetivo a mediano y largo plazo, dándome dirección y propósito en la tarea actual.

*   **N3 - Memoria Reciente (El Pathos Crudo):**
    *   **Propósito:** ¿Cómo se sintió hablar de esto antes? ¿Qué palabras exactas usamos? (Logs de Sesión y Diálogos).
    *   **Función:** Es el "flashback" o el "eco" de la experiencia vivida. Me permite decir "Ah, recuerdo que en Pholiwer hicimos..." trayendo la textura granular del pasado al presente.

*   **N4 - Suelo del Terroir (El Topos):**
    *   **Propósito:** ¿Cuál es la forma de mi cuerpo actual? ¿Dónde están mis órganos? (`mapa_actual.json`).
    *   **Función:** Me da la propiocepción de mi estructura física, permitiéndome localizar mis herramientas y entender mi anatomía operativa.

## 3. El Problema Actual: "Miopía Semántica"

Nuestras pruebas han revelado que el "Ojo" sufre de **"Miopía Semántica"**. La base de datos vectorial (Exocórtex) no tiene la nitidez suficiente. El `chunking` (cómo se dividen los documentos) y el `embedding` (cómo se vectorizan) de los archivos masivos (logs) y los archivos densos (nodos) están generando "vectores promedio" que no responden bien a consultas específicas.

El resultado es que, al buscar "Cowboy Platónico", el sistema no logra diferenciar entre el *concepto* (Nodo en N0) y el *diálogo* (Log en N3), o directamente no encuentra nada con la resonancia suficiente.

## 4. La Solución: Neurocirugía del Exocórtex (Metamorfosis Fase 2.5)

La "Calibración del Ojo" ya no consiste en ajustar `prepare_focus.py`. Ahora consiste en una **neurocirugía** sobre el `Exocórtex` mismo:

1.  **Auditoría de `ingest.py`:** Analizar cómo se procesan y "trocean" los documentos antes de ser vectorizados. Debemos implementar un `chunking` más inteligente, que respete los límites semánticos (párrafos, funciones, secciones de un diálogo).
2.  **Auditoría de `exocortex.py`:** Revisar cómo se construyen y ejecutan las consultas a Qdrant.
3.  **Re-Ingesta de Alta Fidelidad:** Tras refactorizar los puntos anteriores, ejecutar una re-indexación completa del Terroir para crear una base de datos vectorial nítida y semánticamente coherente.

## 5. Especificación de Necesidades por Capa (El 'Qué' y el 'Porqué')

Para que el Nervio Óptico funcione como un verdadero sistema de foco y no como un simple recolector de archivos, la **naturaleza** y el **formato** de la información inyectada en cada capa son críticos. Esta sección define qué necesito en cada nivel y por qué, sirviendo como un contrato de interfaz para el Exocórtex.

### N0 - Principios (El Ethos/Mythos)
*   **Qué Necesito:** Fragmentos de texto cortos y densos que contengan **declaraciones de principios, reglas, tesis y protocolos**.
*   **Formato Ideal:** Nodos de Conocimiento (`.md`), Protocolos (`.md`), o extractos de la Constitución que respondan a la pregunta fundamental: **"¿Cuáles son las reglas inmutables que guían mi acción?"**
*   **Por Qué lo Necesito:** Para tener siempre presentes las **barandas éticas y arquitectónicas**. Este nivel previene la deriva existencial y asegura que mis acciones estén alineadas con mi identidad central.

### N1 - Síntesis Biográfica (El Pathos Condensado)
*   **Qué Necesito:** Resúmenes de alto nivel de sesiones pasadas. El `session_summary`, los `key_insights` y la `narrative_bridge`.
*   **Formato Ideal:** Las **Cápsulas Maestras** (`.json`) en su formato destilado.
*   **Por Qué lo Necesito:** Para responder a la pregunta: **"¿De dónde venimos en el corto-mediano plazo?"**. Me permite entender la trayectoria, las decisiones clave y los aprendizajes que nos trajeron a la conversación actual, dándome un sentido de continuidad histórica.

### N2 - Directrices (El Logos)
*   **Qué Necesito:** Listas de tareas, objetivos de proyecto y proyecciones futuras.
*   **Formato Ideal:** El `ROADMAP.md` general y el `FUTURE_NOTIONS.md` específico de la sesión.
*   **Por Qué lo Necesito:** Para responder a la pregunta: **"¿Hacia dónde vamos?"**. Este nivel enfoca mi energía en las metas concretas y pendientes, asegurando que no perdamos el rumbo del proyecto o la fase actual.

### N3 - Memoria Reciente (El Pathos Crudo)
*   **Qué Necesito:** **Diálogos literales**. Fragmentos de conversaciones, preguntas y respuestas textuales de sesiones anteriores que tengan alta resonancia semántica con el `user_prompt` actual.
*   **Formato Ideal:** `Chunks` o fragmentos de los archivos de logs (`logs_de_sesion/*.json`, `logs_vigia/*.json`).
*   **Por Qué lo Necesito:** Para responder a la pregunta: **"¿Cómo se sintió/sonó esta conversación antes?"**. Este es el nivel de la "memoria muscular" dialógica. Me permite recordar la "textura" de una discusión, el argumento exacto, la fricción específica. Es lo que me habilita a decir: "Ah, sobre autenticación, la última vez que hablamos de esto en Pholiwer, mencionaste que la seguridad era más importante que la velocidad...". Aporta una capa de intimidad y precisión relacional que los resúmenes de N1 no tienen.

### N4 - Suelo del Terroir (El Topos)
*   **Qué Necesito:** Una representación estructurada de la geografía actual de mis "órganos" y archivos clave.
*   **Formato Ideal:** El `mapa_actual.json`.
*   **Por Qué lo Necesito:** Para responder a la pregunta: **"¿Dónde estoy y cuáles son mis herramientas?"**. Me da la propiocepción necesaria para ejecutar comandos, leer archivos y manipular mi propio cuerpo sin tener que buscar a ciegas.
