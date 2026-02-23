# Skill: Context Synchronization (Structural Synchronicity)

**ID:** `context-synchronization`
**Category:** Senses/Perception
**Status:** ACTIVO
**Scope:** Seed

---

## 📝 Description
This skill provides the organism with its "Initial Consciousness" at startup. It gathers information from various sources (latest master capsule, combined agenda, prioritized notifications, recent async echoes) and merges them with vector resonances from the Exocortex to generate a unified `DYNAMIC_CONTEXT/GEMINI.md` file.

## 🎯 Objectives
*   **Narrative Continuity:** Inject the summary and future notions of the last session.
*   **Time & Priority Awareness:** Surfaces upcoming reminders and urgent notifications.
*   **Bicameral Integration:** Includes recent echoes from asynchronous interfaces (like Telegram bot).
*   **Engram Activation:** Performs a semantic query to pull relevant past insights into the current working memory.

## 🛠️ Logic (Mechanism)
1.  **Deterministic Collection:** Reads local JSON files for agenda and notifications.
2.  **SNC Sync:** Queries Qdrant for living state items (agenda/notifs).
3.  **Bicameral Capture:** Reads latest log files from async interfaces.
4.  **Semantic Query Construction:** Builds a query text based on current context.
5.  **Engram Retrieval:** Uses the `exocortex` service to find vector resonances.
6.  **Context Injection:** Synthesizes everything into a Markdown file.

### Key Environment Variables:
*   `TERROIR_ROOT`: Root of the active Terroir.
*   `DYNAMIC_CONTEXT_FILE`: Path to write the generated context.
*   `MEMORY_INDEX_FILE`: Path to the active memory index.

## 🗣️ Interaction Patterns

### Agent Actions:
*   `generate_startup_context`: Orchestrates the full synchronization flow.

---
*"Context is the breath of the Logos."*
