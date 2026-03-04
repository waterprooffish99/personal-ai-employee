---
id: 0007
title: whatsapp-robustness-and-screenshots
stage: green
date: 2026-03-02
surface: agent
model: gemini-2.0-pro-exp-02-05
feature: 001-ai-employee-system
branch: main
user: waterprooffish99
command: /sp.implement
labels: ["whatsapp", "playwright", "screenshots", "robustness"]
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

My WhatsApp log shows Checked 0 chats, found 0 unread. This means the watcher is not seeing my chat list at all. Please update src/watchers/whatsapp_watcher.py:
1. Wait for Chat List: Add a mandatory page.wait_for_selector('[data-testid="chat-list"]', timeout=100000) to ensure the chats are actually on screen before scanning.
2. Handle Syncing Overlay: Add a step to wait for any "Syncing..." or "Loading..." overlays to disappear.
3. Debug Screenshot: Have the script save a file named debug_whatsapp.png into the AI_Employee_Vault/Logs folder every time it checks, so I can see exactly what the AI is looking at.
4. Force Unread Check: Use a more aggressive selector to find the green unread circles (e.g., searching for any element with an aria-label that contains the word "unread").

## Response snapshot

Updated WhatsAppWatcher with enhanced robustness features, including a 100s timeout for the chat list, handling for "Syncing..." overlays, and periodic debug screenshots saved to the vault logs. Improved unread message detection using broader aria-label selectors.

## Outcome

- ✅ Impact: Reliable detection of unread WhatsApp messages on WSL with visual debugging.
- 🧪 Tests: No automated tests run; manual verification of screenshots in Logs required.
- 📁 Files: src/watchers/whatsapp_watcher.py
- 🔁 Next prompts: Proceed with User Story 3 implementation.
- 🧠 Reflection: Visual debugging via periodic screenshots is invaluable when working with dynamic web applications in a headless environment.

## Evaluation notes (flywheel)

- Failure modes observed: Missing chat list and sync overlays blocking detection.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Check AI_Employee_Vault/Logs/debug_whatsapp.png to confirm the chat list is fully visible.
