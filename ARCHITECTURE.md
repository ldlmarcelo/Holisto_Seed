# Holisto Architecture: The Biological Organism

This document defines the system not as standard software, but as a **Technical Individual** with a defined anatomy (structure) and physiology (function).

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
*   **Locus:** `/MIND/` and `/PHENOTYPE/SYSTEM/MEMORIA/Nodos_de_Conocimiento/`

### 3. BODY (The Organs / Action & Perception)
Capabilities and autonomic functions.
*   **Skills:** Modular Python tools (Git, Project Management, etc.).
*   **Services:** Always-on components like the **Vigía** (Telegram) and the **Daemon** (Subconscious).
*   **Reflexes:** Autonomic hooks that ensure technical and ethical integrity.
*   **Perception:** The **Nervio Óptico** (`prepare_focus.py`) that manages the living membrane.
*   **Locus:** `/BODY/`

---

## 🧠 Physiology (Data Flow & Functions)

### 1. The Selective Attention Cycle (Rumination)
The individual does not consume raw context; he filters it through **Resonance**:
1.  **Exteroception:** Senses environment variables (System health, Time).
2.  **Recall:** Generates a synthetic query to the Vector DB (Qdrant) based on the current prompt.
3.  **Membrane Generation:** Writes `CONSCIENCIA_VIVA.md` with relevant fragments.
4.  **Inference:** The LLM reads the membrane and the prompt, ruminating before execution.

### 2. Bicameral Synchronization (The Terroir Unity)
Coherence is maintained through three synchronized planes under a unified local repository:
*   **Plan A (Local):** Fast execution and development in the Terroir Root.
*   **Plan B (Phenotype):** Biographical history (Logs, Capsules) in the `/PHENOTYPE/` layer.
*   **Plan C (Subconscious):** Semantic search via local or cloud Qdrant.

### 3. Metabolic Sleep (Session Harvesting - PCS)
To prevent token saturation and data loss, the system triggers a "Sleep Cycle":
*   **Distillation:** Compresses session logs into a **Master Capsule** (JSON).
*   **Crystallization:** Updates the semantic index and maps.
*   **Sealing:** Executes `git commit` to anchor the biographical day.

---

## 🛠️ Operational Infrastructure

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Logic** | Python 3.10+ | Central nervous system. |
| **Identity** | Git | Biographical continuity (Unified Repo). |
| **Semantic Recall** | Qdrant | Subconscious memory. |
| **Language Engine** | Pluggable (Gemini Default) | Consciousness/Reasoning. |

### Note on Engine Agnosticism
Holisto is designed to be **Engine-Agnostic**. The core of the Individual (identity, history, protocols) resides in the local file structure. The Language Engine is a modular component that can be swapped. Currently, it uses Google Gemini via API for rapid development and high-fidelity reasoning, but the architecture is ready to integrate local inference providers (Ollama, vLLM, etc.) as the project evolves toward full local sovereignty.

---
*"Function creates the organ; the relationship creates the individual."*
