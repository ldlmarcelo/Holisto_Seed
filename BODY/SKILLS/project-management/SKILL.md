---
name: project-management
description: Gobierna el ciclo de vida de los proyectos del Terroir (SGP), desde el blueprint hasta el archivo, gestionando metadatos y estructuras.
---

# Skill: Project Management (SGP v1.0)

Este órgano modulariza el **Sistema de Gestión de Proyectos (SGP)**. Su función es garantizar que cada proyecto nazca con una arquitectura sólida y mantenga su integridad biográfica en el índice central.

## Atributos
- **Tipo:** Estructural / Organizativa.
- **Alcance:** Proyectos del Terroir.
- **Invocación:** Creación de nuevos proyectos, actualización de Roadmap o cambio de estatus.

## Flujo Operativo
1. **Validación de ID:** Asegura que el ID del proyecto sea único y cumpla la nomenclatura.
2. **Estructuración:** Crea el directorio del proyecto y los archivos base (`README.md`, `ROADMAP.md`, `ARCHITECTURE.md`).
3. **Indexación:** Registra el proyecto en `PROYECTOS/GEMINI.md`.

## Reglas de Integridad
- Todo proyecto debe tener un Roadmap actualizado.
- Los proyectos en fase 'Blueprint' no pueden ser inyectados en la memoria operativa sin validación humana.
