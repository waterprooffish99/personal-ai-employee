---
id: 0002
title: whatsapp-auth-and-loop-fix
stage: green
date: 2026-03-02
surface: agent
model: gemini-2.0-pro-exp-02-05
feature: 001-ai-employee-system
branch: main
user: waterprooffish99
command: /sp.implement
labels: ["whatsapp", "auth", "session", "loop"]
links:
  spec: specs/001-ai-employee-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/watchers/auth_whatsapp.py
  - src/watchers/whatsapp_watcher.py
  - src/orchestrator.py
tests:
  - None
---

## Prompt

/sp.implement

PHASE: WHATSAPP AUTHENTICATION & SESSION FIX

The WhatsApp watcher is currently running invisibly (headless) and exiting too fast. We need to create a dedicated script to scan the QR code and save the session.

1. CREATE AUTH SCRIPT:
   - Create `src/watchers/auth_whatsapp.py`.
   - This script must launch Playwright with `headless=False` (visible mode).
   - It should point to a persistent directory: `AI_Employee_Vault/.sessions/whatsapp`.
   - It should open `https://web.whatsapp.com` and wait for the user to press 'Enter' in the terminal after scanning.

2. UPDATE WHATSAPP WATCHER:
   - Update `src/watchers/whatsapp_watcher.py` to use the SAME session directory: `AI_Employee_Vault/.sessions/whatsapp`.
   - Ensure it uses `headless=True` for normal operation so it doesn't pop up every minute.

3. UPDATE ORCHESTRATOR:
   - Ensure the orchestrator can run in a "loop" rather than a "single cycle" so the watcher stays active.

After generating the code, give me the exact command to run the auth script so I can scan my QR code.

## Response snapshot

Implemented a dedicated WhatsApp authentication script to handle QR code scanning and persistent sessions. Updated the WhatsApp watcher to use this shared session in headless mode and enhanced the orchestrator to support continuous loop operation.

## Outcome

- ✅ Impact: WhatsApp session persistence and multi-watcher loop mode enabled.
- 🧪 Tests: No automated tests run; manual verification with auth script required.
- 📁 Files: src/watchers/auth_whatsapp.py, src/watchers/whatsapp_watcher.py, src/orchestrator.py
- 🔁 Next prompts: Proceed with User Story 3 implementation.
- 🧠 Reflection: Clear separation of auth and operation modes is essential for web-based messaging integrations.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Integrate Odoo MCP for accounting tasks.
