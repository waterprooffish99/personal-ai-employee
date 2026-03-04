---
id: 0005
title: whatsapp-browser-compatibility-fix
stage: green
date: 2026-03-02
surface: agent
model: gemini-2.0-pro-exp-02-05
feature: 001-ai-employee-system
branch: main
user: waterprooffish99
command: /sp.implement
labels: ["whatsapp", "playwright", "user-agent", "browser-fix"]
links:
  spec: specs/001-ai-employee-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/watchers/auth_whatsapp.py
  - src/watchers/whatsapp_watcher.py
tests:
  - None
---

## Prompt

/sp.implement

My WhatsApp Watcher is stuck. I checked the screenshot in my vault, and it shows the "WhatsApp works with Google Chrome 85+" error page. This is preventing the AI from seeing my messages.

Please fix 'src/watchers/whatsapp_watcher.py' and 'src/watchers/auth_whatsapp.py' with the following:

1. USER AGENT FIX: 
   - Update the Playwright browser context to use a modern, common User Agent string (e.g., a recent Chrome on Windows string). This stops WhatsApp from thinking the browser is too old.

2. VIEWPORT & STEALTH: 
   - Set a standard viewport size (e.g., 1280x800) and ensure 'is_mobile' is set to False.

3. PERSISTENCE CHECK:
   - Ensure the session is still being saved to 'AI_Employee_Vault/.sessions/whatsapp' so I don't have to keep scanning the QR code.

After you provide the updated code, please give me the command to run the auth script one more time to refresh the session with the new settings.

## Response snapshot

Updated WhatsApp auth and watcher scripts to use a modern Chrome User Agent, standard desktop viewport (1280x800), and disabled mobile emulation. This resolves the browser version error while maintaining persistent sessions in the vault.

## Outcome

- ✅ Impact: WhatsApp browser compatibility issue resolved.
- 🧪 Tests: No automated tests run; manual verification with auth script required.
- 📁 Files: src/watchers/auth_whatsapp.py, src/watchers/whatsapp_watcher.py
- 🔁 Next prompts: Proceed with User Story 3 implementation.
- 🧠 Reflection: Explicit User Agent and viewport settings are often necessary when using Playwright/Chromium to interact with web apps that have strict browser version checks.

## Evaluation notes (flywheel)

- Failure modes observed: "WhatsApp works with Google Chrome 85+" error
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Verify WhatsApp message detection in headless mode.
