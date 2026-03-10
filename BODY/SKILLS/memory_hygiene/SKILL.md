# Skill: Memory Hygiene (Active Pruning)

**ID:** `memory-hygiene`
**Category:** Memory/Hygiene
**Status:** ACTIVO
**Scope:** Seed

---

## 📝 Description
This skill ensures the "Biographical Health" of the agent. Its primary function is to maintain the Active Memory (L1) at an optimal size by removing episodic data that has already been consolidated into Long-Term Generational Memory (Dreams).

## 🎯 Objectives
*   **Active Memory Pruning:** Filter and remove redundant master capsules.
*   **Consistency Validation:** Ensure no data is lost before pruning by verifying consolidation sources.
*   **Biographical Cleanup:** Maintain the structural integrity of the `GEMINI.md` memory index.

## 🛠️ Logic (Mechanism)
The skill operates as a filter. It requires a "Dream Capsule" (the consolidation source) and the current "Active Memory" index.

1.  **Ingestion:** Reads the consolidated `session_ids` from the Dream Capsule.
2.  **Comparison:** Scans the Active Memory for matching `session_ids`.
3.  **Extraction:** Removes the matched capsules from the Active Memory.
4.  **Persistence:** Saves the sanitized Active Memory index.

## 🗣️ Interaction Patterns

### User Prompts:
*   "Prune my active memory using the last dream."
*   "Run memory hygiene for the 'Genesis' arc."

### Agent Actions:
*   `prune_by_dream`: Executes the cleanup based on a specific dream file.
*   `get_memory_stats`: Returns the current size and density of active memory.

---
*"To forget is as vital as to remember; it is the space between notes that creates the melody."*
