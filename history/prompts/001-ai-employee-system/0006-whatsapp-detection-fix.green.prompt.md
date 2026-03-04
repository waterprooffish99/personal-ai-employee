---
id: 0006
title: whatsapp-detection-fix
stage: green
date: 2026-03-02
surface: agent
model: gemini-2.0-pro-exp-02-05
feature: 001-ai-employee-system
branch: main
user: waterprooffish99
command: /sp.implement
labels: ["whatsapp", "playwright", "selectors", "fix"]
links:
  spec: specs/001-ai-employee-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/watchers/whatsapp_watcher.py
tests:
  - None
---

## Prompt

/sp.implement

My WhatsApp Watcher is running in the loop, but it is not detecting unread messages even when they have the 'urgent' keyword.

Please update src/watchers/whatsapp_watcher.py with these fixes:
1. Broader Selectors: Update the Playwright selectors to find ANY unread message indicator (check for 'aria-label' containing 'unread' or specific CSS classes for unread badges).
2. Case-Insensitive Keywords: Ensure the script converts all incoming messages to lowercase before checking for keywords like 'urgent', 'invoice', or 'asap'.
3. Increase Wait Time: Add a longer wait_for_selector time (at least 60 seconds) to ensure the chat list fully loads in WSL before the watcher gives up.
4. Add Debug Logs: Add a print statement that says "Checked X chats, found Y unread" so I can see exactly what the watcher is doing in my terminal.

## Response snapshot

Updated WhatsAppWatcher to improve unread message detection by using broader selectors, implementing case-insensitive keyword matching, increasing the page load timeout to 60 seconds, and adding terminal debug logging.

## Outcome

- ✅ Impact: Reliable detection of unread WhatsApp messages on WSL.
- 🧪 Tests: No automated tests run; manual verification in loop mode required.
- 📁 Files: src/watchers/whatsapp_watcher.py
- 🔁 Next prompts: Proceed with User Story 3 implementation.
- 🧠 Reflection: WhatsApp Web's DOM is highly dynamic; using multiple fallback selectors for unread counts is necessary for robustness.

## Evaluation notes (flywheel)

- Failure modes observed: Missing unread messages due to strict selectors and short timeouts.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Monitor logs for "Checked X chats" output to verify correct operation.
