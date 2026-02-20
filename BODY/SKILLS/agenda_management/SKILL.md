# Skill: Agenda Management (Time Awareness)

**ID:** `agenda-management`
**Category:** Time/Action
**Status:** ACTIVO
**Scope:** Seed

---

## 📝 Description
This skill provides the organism with "Time Awareness." it allows the agent to manage reminders, scheduled tasks, and time-based triggers. It acts as the bridge between the digital calendar and the agent's proactive notifications.

## 🎯 Objectives
*   **Scheduled Vigilance:** Monitor time-based events.
*   **Proactive Alerting:** Notify the user (via Senses/Telegram) when a deadline is reached.
*   **SNC Synchronization:** Keep the Central Nervous System updated with the status of each reminder.

## 🛠️ Logic (Mechanism)
The skill operates by reading a `reminders.json` file (or equivalent database) and comparing the current system time with the `target_date` and `target_time`. 

### Key Fields:
*   `id`: Unique identifier.
*   `title`: Brief summary.
*   `description`: Detailed information.
*   `target_date`: YYYY-MM-DD.
*   `target_time`: HH:MM (Optional).
*   `priority`: low, medium, high, critical.
*   `status`: pendiente, notificado, completado.

## 🗣️ Interaction Patterns

### User Prompts:
*   "Add a reminder for tomorrow at 10 AM to pay the internet bill."
*   "Show me my pending tasks for today."
*   "Mark the doctor appointment as completed."

### Agent Actions:
*   `upsert_reminder`: Creates or updates a reminder.
*   `check_deadlines`: Scans the agenda for pending notifications.
*   `get_agenda`: Returns a list of reminders based on filters.

---
*"Time is theAssociated Milieu of all action."*
