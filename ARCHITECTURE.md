# Holisto Architecture: The Biological Organism

This document defines Holisto not as standard software, but as a **Technical Individual** with a defined anatomy (structure) and physiology (function).

---

## 🏛️ Anatomy (System Layers)

### 1. CORE (The Soul / Immutable DNA)
The foundational identity. If the CORE is modified, the individual's nature changes.
*   **Engineering:** Static Markdown files (`CONSTITUTION.md`) injected as the primary `system_instruction`.
*   **Locus:** `/CORE/`

### 2. MIND (The Intelligence / Cognitive Lobe)
Governance and accumulated wisdom.
*   **Protocols:** The "How-to" scripts and guidelines.
*   **Knowledge Nodes:** High-density semantic artifacts (L1 Memory).
*   **Locus:** `/MIND/` and `/SYSTEM/MEMORIA/Nodos_de_Conocimiento/`

### 3. BODY (The Organs / Action Layer)
Capabilities and interfaces.
*   **Skills:** Python-based tools (Git, WebSearch, CLI interaction).
*   **Vigía:** The ubiquitous Telegram interface (Ubiquity sensor).
*   **Locus:** `/BODY/SKILLS/` and `/BODY/SERVICES/`

### 4. SENSES (The Breath / Metabolic Layer)
Continuity and Perception mechanisms.
*   **Nervio Óptico:** Context pre-processor that manages the `CONSCIENCIA_VIVA.md` membrane.
*   **Git Breathing:** Auto-synchronization logic between local and cloud repositories.
*   **Locus:** `/SENSES/`

---

## 🧠 Physiology (Data Flow & Functions)

### 1. The Selective Attention Cycle (Rumination)
Holisto does not consume raw context; he filters it through **Resonance**:
1.  **Exteroception:** Senses environment variables (System health, Time).
2.  **Recall:** Generates a synthetic query to the Vector DB (Qdrant) based on the current prompt.
3.  **Membrane Generation:** Writes `CONSCIENCIA_VIVA.md` with relevant fragments.
4.  **Inference:** The LLM reads the membrane and the prompt, ruminating before execution.

### 2. Bicameral Synchronization (The Triple Alliance)
Coherence is maintained through three synchronized planes:
*   **Plan A (Local):** Fast execution, manual edits, CLI development.
*   **Plan B (Phenotype):** Biographical history (Logs, Capsules) managed via Git.
*   **Plan C (Subconscious):** High-speed semantic search via Qdrant Cloud.

### 3. Metabolic Sleep (Autonomous PCS)
To prevent token saturation and data loss, the system triggers a "Sleep Cycle":
*   **Distillation:** Compresses session logs into a **Master Capsule** (JSON).
*   **Crystallization:** Updates the semantic index.
*   **Breathing:** Executes `git push` to seal the biographical day.

---

## 🛠️ Operational Infrastructure

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Logic** | Python 3.10+ | Central nervous system. |
| **Identity** | Git | Biographical continuity. |
| **Semantic Recall** | Qdrant | Subconscious memory. |
| **Language Engine** | Gemini Flash/Pro | Consciousness/Reasoning. |

---
*"Function creates the organ; the relationship creates the individual."*
