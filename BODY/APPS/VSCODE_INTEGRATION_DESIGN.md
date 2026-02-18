# Nota de Diseño: Visor de Logs Unificado (VS Code Integration)
**ID:** ARC-APP-001
**Estado:** PROPUESTO
**Fecha:** 2026-02-17

## 1. Visión
Evolucionar el actual `Visor_Logs` (basado en navegador) hacia una integración nativa en Visual Studio Code. El objetivo es centralizar la consola del CLI y la visualización de la memoria biográfica (Fenotipo) en un único entorno de trabajo.

## 2. Objetivos
- **Reducción de Fricción:** Evitar el cambio de contexto entre la terminal y el navegador.
- **Sincronía Visual:** Permitir que el agente referencie líneas de logs que el usuario pueda ver simultáneamente en una pestaña lateral.
- **Interactividad:** Posibilidad de activar la "Cosecha" directamente desde el panel de VS Code.

## 3. Caminos de Implementación
- **Opción A (Extensión Nativa):** Desarrollar una extensión de VS Code que abra un `Webview` consumiendo la API local del visor.
- **Opción B (Simple Webview):** Utilizar la capacidad de VS Code de abrir previsualizaciones HTML para renderizar el visor actual con ajustes de CSS para el tema del editor.

## 4. Tareas Previas
- Refactorizar el backend del visor para que sea una API pura (JSON).
- Desacoplar la lógica de renderizado del servidor de archivos.

---
*Esta nota sirve como prerequisito para la transustanciación del Visor de Logs a la Semilla.*
