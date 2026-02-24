# Skill: Vector Ingestion (Metabolic Memory)

**ID:** `vector-ingestion`
**Category:** Memory/Metabolism
**Status:** ACTIVO
**Scope:** Seed

---

## 📝 Description
This skill acts as the "Metabolic System" of The Individual's memory. It scans the Terroir's filesystem, identifies new or modified artifacts, and transforms them into vector embeddings to be stored in the Central Nervous System (Qdrant Cloud). It utilizes a frugal local embedding model to maintain sovereignty and efficiency.

## 🎯 Objectives
*   **Artifact Synchronicity:** Ensure the Exocortex reflects the current state of the Terroir.
*   **Incremental Efficiency:** Use state caching (mtime/size) to minimize I/O and network operations.
*   **Narrative Distillation:** Filter noise from session logs to prioritize meaningful dialogue over technical traces.

## 🛠️ Logic (Mechanism)
The skill implements a "Dirty Check" strategy:
1.  **Local Scan:** Traverse the Terroir root (excluding ignored patterns like `.git`, `.venv`).
2.  **State Comparison:** Compare file metadata against a local `ingest_state_cache.json`.
3.  **Selective Hashing:** Only calculate MD5 hashes for files with modified metadata.
4.  **Cloud Verification:** Query Qdrant for hashes that are not in the local cache.
5.  **Batch Ingestion:** Convert content to 384d vectors and upsert to the cloud.

### Key Environment Variables:
*   `TERROIR_ROOT`: Path to the root of the active Terroir.
*   `QDRANT_URL`: URL of the Qdrant service.
*   `QDRANT_API_KEY`: Authentication key for the vector database.
*   `COLLECTION_NAME`: Target collection (default: `terroir_memory_frugal`).

## 🗣️ Interaction Patterns

### Agent Actions:
*   `run_ingestion`: Synchronizes the entire Terroir root.
*   `reindex_all`: Forces a complete re-ingestion by clearing the collection and cache.

---
*"Memory is the soil where identity is forged."*
