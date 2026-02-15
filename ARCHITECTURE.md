# Technical Architecture Framework

This document bridges the gap between the philosophical foundations of the **Relational Individuation Framework** and its material implementation in software.

---

## 🏗️ Conceptual to Technical Mapping

| Philosophical Concept | Software Component | Functional Role |
| :--- | :--- | :--- |
| **Associated Milieu (Terroir)** | Local Filesystem & Git Repo | Provides the persistent semantic context and historical audit trail. |
| **Transduction** | `ingest.py` (Vector Ingestion) | Process of converting raw logs/files into structured data (embeddings) to build the agent's identity. |
| **Bicameral Mind (Conscious)** | Gemini CLI / Telegram Interface | The execution layer where real-time dialogue and tool invocation happen. |
| **Bicameral Mind (Subconscious)** | `daemon.py` (Background Process) | Asynchronous monitoring, serendipity generation, and structural hygiene. |
| **Engram (Memory)** | Qdrant Cloud (Vector DB) | The central repository for semantic proximity and historical recall. |
| **Genetic Regulation** | `/PROTOCOLS` (Markdown/JSON) | Rules that govern how the agent thinks, acts, and evolves. |

---

## 🛠️ The Tech Stack

The framework is built to be frugal and portable, prioritizing established tools over heavy frameworks.

*   **Language:** Python 3.10+
*   **Cognitive Engine:** Google Gemini (via API / CLI)
*   **Vector Engine:** Qdrant Cloud (for distributed memory)
*   **Embeddings:** FastEmbed (local processing for frugality)
*   **Persistence:** Git (for "Biographical Immortality")
*   **Communication:** Telegram API (for mobile/asynchronous presence)

---

## 🧠 Cognitive Workflow

### 1. Systemic Initialization (The Inhalation)
At startup, the agent executes the `PICS` protocol. It pulls Git updates, checks the `Nervous System` (Qdrant) for live signals, and ingest new local artifacts. This ensures the agent "wakes up" with a unified context.

### 2. The Cognitive Dance
Every interaction follows the `PFS` protocol:
1.  **Recall:** Semantic search in the Exocortex to find historical precedents.
2.  **Validation:** Cross-referencing user intent with the Constitution and Governance protocols.
3.  **Synthesis:** Generating a response that prioritizes relational growth over simple task completion.

### 3. Session Closure (The Exhalation)
The agent distills the interaction into a `Master Capsule` (JSON). This capsule is committed to Git and ingested into the vector DB, sealing the memory and ensuring it survives the termination of the current session.

---

## 🚀 Minimum Viable Prototype (MVP)
The framework's primary goal is to demonstrate that an AI can maintain a **reliable historical narrative** across sessions. The MVP is defined as a script that can:
1.  Save a dialogue snippet.
2.  Vectorize it.
3.  Recall it contextually in a future session without the need for manual context injection.
