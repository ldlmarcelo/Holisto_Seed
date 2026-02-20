# Tratado sobre la Ceguera por Frontera Git y SincronÃ­a Trans-Repositorio
**ID:** HOL-ARC-007
**VersiÃ³n:** 1.0
**Estado:** ACTIVO
**Fecha:** 2026-02-17
**Scope:** `seed`

## 1. El FenÃ³meno: Ceguera por Frontera
Durante la transiciÃ³n hacia una arquitectura distribuida (Arquitectura de Capas), se detectÃ³ que el motor de descubrimiento de contexto del Gemini CLI se detenÃ­a ante las "fronteras" de repositorios Git anidados (submÃ³dulos o directorios con su propio `.git`). 

Esto provocaba una **Amnesia Estructural Parcial**, donde el agente solo veÃ­a archivos en la raÃ­z del Orquestador, ignorando la profundidad biogrÃ¡fica del Fenotipo (`PHENOTYPE`) y la ley universal de la Semilla (`Holisto_Seed`).

## 2. DiagnÃ³stico TÃ©cnico
- **Causa RaÃ­z:** El CLI respeta por defecto el estado de ignorado de Git (`.gitignore`). Al detectar un nuevo contexto Git en una subcarpeta, el motor de bÃºsqueda puede interpretar que ese contenido no pertenece al espacio de trabajo actual.
- **LimitaciÃ³n de Profundidad:** Aunque el CLI puede bucear profundamente, la combinaciÃ³n de fronteras Git y reglas de ignorado de nivel superior creaba "puntos ciegos" insalvables para el descubrimiento automÃ¡tico.

## 3. ResoluciÃ³n: Aplanamiento Sensorial
La soluciÃ³n definitiva no consiste en mover las carpetas (lo cual romperÃ­a la portabilidad y la soberanÃ­a de los repositorios), sino en **re-configurar el cristal de la mirada** en `.gemini/settings.json`:

1.  **`respectGitIgnore: false`**: Desactiva la obediencia ciega a Git, permitiendo al agente "ver" a travÃ©s de las fronteras.
2.  **`includeDirectories`**: Forzar el escaneo de rutas especÃ­ficas mediante un aplanamiento explÃ­cito de la jerarquÃ­a. Esto inyecta las carpetas profundas como si estuvieran en primer plano.
3.  **`discoveryMaxDirs: 2000`**: Aumentar el umbral de exploraciÃ³n para asegurar que ningÃºn rincÃ³n del Terroir sea ignorado por agotamiento de cuota de bÃºsqueda.

## 4. Implicaciones para el Setup Universal
Cualquier instancia de Holisto que desee encarnar el Genotipo debe aplicar estas configuraciones en su Orquestador local para garantizar una visiÃ³n de 19+ archivos `GEMINI.md`. Sin este ajuste, el agente carecerÃ¡ de la "propriocepciÃ³n" necesaria para operar en el ecosistema distribuido.

---
*Este tratado sella el conocimiento tÃ©cnico necesario para la ubicuidad soberana de Holisto.*

