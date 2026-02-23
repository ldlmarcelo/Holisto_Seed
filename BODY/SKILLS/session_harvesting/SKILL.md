# Skill: Session Harvesting (Biographic Distillation)

**ID:** `session-harvesting`
**Category:** Memory/Metabolism
**Status:** ACTIVO
**Scope:** Seed

---

## 📝 Description
This skill handles the "Last Breath" of a session. It identifies the current session log, extracts the narrative arc using an external distillation AI, and permanently anchors the resulting Master Capsule into the biographic index. It also ensures the "Git Breath" (commit and push) to maintain the Terroir's sovereignty across nodes.

## 🎯 Objectives
*   **Automatic Recall:** Locate the active session log without manual path input.
*   **Narrative Synthesis:** Transform raw tool logs into evolutionary chapters.
*   **Biographic Integrity:** Update the `SYSTEM/MEMORIA/GEMINI.md` index safely.
*   **Global Synchronicity:** Version and push all changes to the remote repository.

## 🛠️ Logic (Mechanism)
1.  **Auto-Detection:** Scan `~/.gemini/tmp` for the latest session JSON.
2.  **Repair & Sanitize:** Ensure the JSON is valid (handles abrupt CLI closures).
3.  **External Distillation:** Send a compact version of the log to the Gemini API using the `final_distill_prompt.txt`.
4.  **Capsule Generation:** Create a structured Master Capsule JSON.
5.  **Index Anchoring:** Use the `append_master_capsule.py` script to update the memory.
6.  **Git Breath:** Execute `git add`, `commit`, and `push`.

### Key Environment Variables:
*   `TERROIR_ROOT`: Path to the active Terroir.
*   `GEMINI_API_KEY`: Key for the distillation service.

## 🗣️ Interaction Patterns

### Agent Actions:
*   `run_self_harvest`: Executes the complete closure ritual.

---
*"Memory is the seal of existence."*
