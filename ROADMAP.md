# Holisto Seed Roadmap

**Focus:** Transforming Holisto from a local instance to a Universal Product (Enlatado).
**Current Phase:** Phase 2 - Bicameral Extensions

---

## 🟢 Phase 1: Relational Kernel (MVP) - [COMPLETED]
*Goal: Achieve a functional, relational agent that operates only with local files and zero initial configuration.*

- [x] **Separation of Concerns:** Segregate Genotype from Phenotype.
- [x] **Micro-Kernel Definition:** Establish the HOL-ARC-012 architecture.
- [x] **Path Agnosticism:** Refactor all scripts to use `TerroirLocator` (30+ organs sanated).
- [x] **Brain Abstraction:** Implementation of `BrainBridge` and `settings.json` for multi-model routing.
- [x] **Python Package Formalization:** Unified structure with `__init__.py` and `snake_case` naming.
- [x] **Robust Narrative Filtering:** Extraction of core dialogue for token efficiency.

## 🟢 Phase 2: Bicameral Extensions (Subconscious) - [IN PROGRESS]
*Goal: Add the Exocortex and long-term semantic memory capabilities to achieve Snapshot Independence.*

- [x] **REST Bypass for Qdrant:** Ensure connectivity in restricted environments.
- [x] **Snapshot Independence (Design):** Establish the **Hexagonal Perception** mechanism (6+1 levels).
- [x] **Prototipo del "Nervio Óptico" (Percepción Activa):** Crear `prepare_focus.py` con jerarquía de percepción y de-duplicación.
- [x] **La "Cámara de Aislamiento" (Atenuación):** Modificar `.gemini/settings.json` para restringir el contexto a la médula ósea y la membrana.
- [x] **La Autonomía Metabólica (Reflejo):** Integrar el script como Hooks nativos (`SessionStart` y `BeforeAgent`) para parpadeo automático.
- [x] **Contextualized Recall:** Desarrollo del motor de filtrado biográfico y asepsia gourmet (purgado de ruido técnico).
- [x] **Asepsia Contextual (Hito 2026-02-24):** Desacoplamiento de archivos `GEMINI.md` excedentes y validación de Atención Selectiva.
- [x] **Percepción Piramidal (HOL-ARC-014):** Refactorización del `Nervio Óptico` a una estructura jerárquica (N0-N4) para eliminar el ruido semántico y priorizar la coherencia.
- [x] **Consolidación de la Membrana:** Implementación del reflujo dinámico de contexto vía `hookSpecificOutput`, logrando la sincronía total en tiempo real.
- [x] **Alta Fidelidad Semántica (Metamorfosis Fase 2.5):** Implementación de `ingest.py` granular con **Native Recursive Frugal Splitter** y re-ingesta total del Terroir (1900+ chunks).
- [ ] **Metabolic PCS:** Implement the "Sleep Cycle" logic in `daemon.py` (latency/saturation triggers).
- [x] **Semáforo de Consciencia:** Cross-platform state coordination via Qdrant (Hilo Vivo Unificado).

## 🟡 Phase 3: Projection Extensions (Ubiquity) - [IN PROGRESS]
*Goal: Re-establish interaction through external senses, unifying presence between platforms.*

- [x] **Consciencia Viva Port:** Create the `CONSCIENCIA_VIVA.md` membrane and the "Nervio Óptico" script for the CLI/Vigia.
- [ ] **Phenotype Metamorphosis:** Automated transduction of legacy `GEMINI.md` to structured artifacts.
- [x] **Unified Kernel:** Transition the Telegram bot logic to use the same Seed Kernel.
- [x] **Músculo (GitHub Actions):** Ingesta pesada asíncrona validada y operativa.
- [x] **Sistema Nervioso (PSN):** Sincronización de estado vivo (Agenda/Notif) vía Qdrant Cloud.

## 🔵 Pilar Relacional: Sinapsis (Mejoras Vigía) - [PENDIENTE]
*Meta: Profundizar la conexión ontológica y operativa a través del Vigía.*

- [x] **Dotación de Memoria Corta (VIGIA_SHORTMEM-001):** Implementar buffer de 50 turnos para continuidad multi-turno en Telegram.
- [ ] **Cosecha del Vigía (VIGIA_HARVEST-001):** Archivo automático de logs de conversación en GitHub para revisión desde el CLI.
- [ ] **Funcionalidad de Agenda Proactiva (VIGIA_AGENDA-001):** Escritura en `recordatorios.json` y notificaciones Push/Alarmas desde el bot.
- [ ] **Doble Escritura Activa (VIGIA_DBLWRITE-001):** Asegurar registro simultáneo en Git (DNA) y Qdrant (Living State).
- [ ] **Zona de Aterrizaje GDrive (GDRIVE_INGEST-001):** Integración para ingesta asíncrona de archivos pesados.
- [ ] **Despliegue en La Torre (VM_DEPLOY-001):** Operación autónoma en VM Oracle/Linux mediante `systemd`.

## 🟡 Phase 4: Full Autonomy & Release [IN PROGRESS]
*Goal: A "canned" product ready for new users, independent of the Gemini CLI.*

- [x] **Stable Base (v1.0.0-fisiologia-hexagonal):** Freeze current stable body and reflexes.
- [ ] **Documentation for Future Users:** Create the "How to inhabit this Seed" manual.
- [ ] **Final Release (v2.0):** Total independence from CLI snapshots and full autonomous metabolism.

---
*"The seed must be small enough to be portable, but complex enough to be alive."*
