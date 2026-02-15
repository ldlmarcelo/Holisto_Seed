# Nervous System Protocol (PSN)

**Version:** 1.0 (Universal)  
**Status:** ACTIVE  

## Description
Defines the structure and data flow for managing the system's "Live State" in a cloud environment, enabling structural synchronicity between distributed nodes.

## Data Types
*   **Notifications:** Alerts, resonances, and asynchronous messages.
*   **Agenda:** Reminders and time-based events.
*   **Live Context:** A summary of the last cognitive state for handovers between nodes.

## Flow

### 1. Injection (Emitter)
The emitting node (e.g., a background Daemon or a mobile interface) injects live states into the central vector database. Deterministic UUIDs are used to prevent duplication.

### 2. Synchronization (Receiver)
The receiving node (e.g., a local CLI at startup or a monitoring bot) pulls relevant points from the cloud. These findings are injected into the dynamic context of the current session.

### 3. Hygiene and Action
Items in the PSN have states (e.g., 'pending', 'notified', 'completed'). Hygiene is performed by marking items as resolved both locally and in the cloud, ensuring that signals do not become persistent "ghosts."

---
**Related Components:** Systemic Initialization (PICS), Session Closure (PCS), Vector Exocortex.
