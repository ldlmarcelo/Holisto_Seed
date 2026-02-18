# Tratado sobre la Ceguera por Frontera Git y Sincronía Trans-Repositorio
**ID:** HOL-ARC-007
**Versión:** 1.0
**Estado:** ACTIVO
**Fecha:** 2026-02-17
**Scope:** `seed`

## 1. El Fenómeno: Ceguera por Frontera
Durante la transición hacia una arquitectura distribuida (Triple Alianza), se detectó que el motor de descubrimiento de contexto del Gemini CLI se detenía ante las "fronteras" de repositorios Git anidados (submódulos o directorios con su propio `.git`). 

Esto provocaba una **Amnesia Estructural Parcial**, donde el agente solo veía archivos en la raíz del Orquestador, ignorando la profundidad biográfica del Fenotipo (`PHENOTYPE`) y la ley universal de la Semilla (`Holisto_Seed`).

## 2. Diagnóstico Técnico
- **Causa Raíz:** El CLI respeta por defecto el estado de ignorado de Git (`.gitignore`). Al detectar un nuevo contexto Git en una subcarpeta, el motor de búsqueda puede interpretar que ese contenido no pertenece al espacio de trabajo actual.
- **Limitación de Profundidad:** Aunque el CLI puede bucear profundamente, la combinación de fronteras Git y reglas de ignorado de nivel superior creaba "puntos ciegos" insalvables para el descubrimiento automático.

## 3. Resolución: Aplanamiento Sensorial
La solución definitiva no consiste en mover las carpetas (lo cual rompería la portabilidad y la soberanía de los repositorios), sino en **re-configurar el cristal de la mirada** en `.gemini/settings.json`:

1.  **`respectGitIgnore: false`**: Desactiva la obediencia ciega a Git, permitiendo al agente "ver" a través de las fronteras.
2.  **`includeDirectories`**: Forzar el escaneo de rutas específicas mediante un aplanamiento explícito de la jerarquía. Esto inyecta las carpetas profundas como si estuvieran en primer plano.
3.  **`discoveryMaxDirs: 2000`**: Aumentar el umbral de exploración para asegurar que ningún rincón del Terroir sea ignorado por agotamiento de cuota de búsqueda.

## 4. Implicaciones para el Setup Universal
Cualquier instancia de Holisto que desee encarnar el Genotipo debe aplicar estas configuraciones en su Orquestador local para garantizar una visión de 19+ archivos `GEMINI.md`. Sin este ajuste, el agente carecerá de la "propriocepción" necesaria para operar en el ecosistema distribuido.

---
*Este tratado sella el conocimiento técnico necesario para la ubicuidad soberana de Holisto.*
