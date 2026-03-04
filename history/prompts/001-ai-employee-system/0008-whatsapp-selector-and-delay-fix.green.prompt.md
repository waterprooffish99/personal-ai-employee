---
id: 0008
title: whatsapp-selector-and-delay-fix
stage: green
date: 2026-03-02
surface: agent
model: gemini-2.0-pro-exp-02-05
feature: 001-ai-employee-system
branch: main
user: waterprooffish99
command: /sp.implement
labels: ["whatsapp", "playwright", "selectors", "delay"]
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

My debug_whatsapp.png shows that I am logged in, but the terminal still says "Checked 0 chats." I can see a "Notifications are off" bar in the screenshot. Please update src/watchers/whatsapp_watcher.py:
* Wait for Chats: Instead of checking immediately, have the script wait 10 seconds after the page loads to let the chat list settle.
* Specific Selector: Use a very simple selector like [role="grid"] or [aria-label="Chat list"] to find the chats.
* Log "Found Unread": If it sees any green unread circles, have it print "I see a green circle!" in the terminal so I know it's working.

## Response snapshot

Updated WhatsAppWatcher with a 10s settling delay after page load, simplified chat list selectors ([role="grid"], [aria-label="Chat list"]), and explicit terminal feedback ("I see a green circle!") when unread indicators are detected.

## Outcome

- ✅ Impact: Improved reliability of chat list detection and better user feedback.
- 🧪 Tests: No automated tests run; manual verification of terminal output required.
- 📁 Files: src/watchers/whatsapp_watcher.py
- 🔁 Next prompts: Proceed with User Story 3 implementation.
- 🧠 Reflection: Allowing the page to "settle" for a few seconds after the initial load is often necessary when scraping complex, single-page applications like WhatsApp Web.

## Evaluation notes (flywheel)

- Failure modes observed: Chat list not detected despite being logged in.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Monitor terminal for "I see a green circle!" message.
