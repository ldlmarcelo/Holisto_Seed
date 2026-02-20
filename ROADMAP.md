# Holisto Seed Roadmap

**Focus:** Transforming Holisto from a local instance to a Universal Product (Enlatado).
**Current Phase:** Phase 1 - Kernel Minimal Viable Product (MVP)

---

## 🟢 Phase 1: Relational Kernel (MVP) - [IN PROGRESS]
*Goal: Achieve a functional, relational agent that operates only with local files and zero initial configuration.*

- [x] **Separation of Concerns:** Segregate Genotype from Phenotype.
- [x] **Micro-Kernel Definition:** Establish the HOL-ARC-012 architecture.
- [ ] **Path Agnosticism:** Refactor all scripts to use relative paths or environment-injected roots.
- [ ] **Local Memory Fallback:** Ensure `prepare_context.py` and `ingest.py` can work with local JSON/Markdown if no Vector DB is present.
- [ ] **Setup Wizard:** Create a simple script to "initialize" a new Terroir from the Seed.

## 🟡 Phase 2: Bicameral Extensions (Subconscious)
*Goal: Add the Exocortex and long-term semantic memory capabilities.*

- [x] **REST Bypass for Qdrant:** Ensure connectivity in restricted environments.
- [ ] **Modular Services:** Move `exocortex.py` and `daemon.py` to a proper `SERVICES` package.
- [ ] **Service Configuration:** Standardize `.env` requirements for cloud features.

## 🟡 Phase 3: Projection Extensions (Senses)
*Goal: Re-establish interaction through external senses (Telegram).*

- [ ] **Vigia Modularization:** Encapsulate the Telegram bot logic as a pluggable extension.
- [ ] **Skill Portability:** Ensure skills in `.gemini/skills` are correctly linked to Seed definitions.

## ⚪ Phase 4: Full Autonomy & Release
*Goal: A "canned" product ready for new users.*

- [ ] **Documentation for Future Users:** Create the "How to inhabit this Seed" manual.
- [ ] **Stable Release (v1.0):** Freeze the codebase and create the first public tag.

---
*"The seed must be small enough to be portable, but complex enough to be alive."*
