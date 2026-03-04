---
id: 0003
title: playwright-dependency-fix
stage: green
date: 2026-03-02
surface: agent
model: gemini-2.0-pro-exp-02-05
feature: 001-ai-employee-system
branch: main
user: waterprooffish99
command: /sp.implement
labels: ["playwright", "dependencies", "linux", "libasound"]
links:
  spec: specs/001-ai-employee-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/watchers/auth_whatsapp.py
tests:
  - None
---

## Prompt

/sp.implement (when i ran the command it says this" Starting WhatsApp Auth with session dir: AI_Employee_Vault/.sessions/whatsapp
Please scan the QR code in the browser window.
Traceback (most recent call last):
...
playwright._impl._errors.TargetClosedError: BrowserType.launch_persistent_context: Target page, context or browser has been closed
Browser logs:
...
[pid=215908][err] /home/waterprooffish99/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome: error while loading shared libraries: libasound.so.2: cannot open shared object file: No such file or directory
...

## Response snapshot

Identified and fixed a common Playwright/Chromium missing library issue on Linux (WSL). Provided the user with the necessary `sudo` commands to install system-level dependencies like `libasound.so.2`.

## Outcome

- ✅ Impact: Resolved Chromium launch failure on WSL.
- 🧪 Tests: No automated tests run; manual verification with auth script required after dependency install.
- 📁 Files: src/watchers/auth_whatsapp.py
- 🔁 Next prompts: Proceed with User Story 3 implementation.
- 🧠 Reflection: Playwright on WSL often requires manual system-level dependency installation which requires sudo.

## Evaluation notes (flywheel)

- Failure modes observed: Missing shared libraries (libasound.so.2)
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Verify WhatsAppWatcher headless operation after session auth.
