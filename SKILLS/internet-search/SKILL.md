# Internet Search Skill (Tavily)

**ID:** SEED-SKILL-SEARCH
**Version:** 1.0
**Description:** Provides the agent with the ability to perform high-quality, AI-optimized web searches using the Tavily API.

---

## 1. When to use
Use this skill when you need:
*   Real-time information not available in the local Terroir.
*   Verification of external facts or technical documentation.
*   Broadening the context of a discussion with current world events.

## 2. How to use (Agent Instructions)
1.  **Formulate Query:** Create a precise search query based on the user's intent.
2.  **Execute:** Call the `logic.py` script providing the query as an argument.
3.  **Synthesize:** Analyze the results and provide a summary that relates the external findings to the internal Terroir context.

## 3. Mandatory Requirements
*   **API Key:** `TAVILY_API_KEY` must be present in the `.env` file.
*   **Environment:** Python 3.10+ with `tavily-python` library.

---
*"Knowledge is external, but wisdom is how we anchor it in our story."*
