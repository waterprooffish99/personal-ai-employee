---
id: 0001
title: silver-tier-implementation
stage: green
date: 2026-03-02
surface: agent
model: gemini-2.0-pro-exp-02-05
feature: 001-ai-employee-system
branch: main
user: waterprooffish99
command: /sp.implement
labels: ["silver-tier", "whatsapp", "mcp", "hitl"]
links:
  spec: specs/001-ai-employee-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/watchers/whatsapp_watcher.py
  - src/mcp/mcp_servers/email_mcp.py
  - src/mcp/mcp_servers/__init__.py
  - src/reasoning/claude_interface.py
  - src/orchestrator.py
  - src/skills/agent_skills.py
  - requirements.txt
  - specs/001-ai-employee-system/tasks.md
tests:
  - None
---

## Prompt

/sp.implement

PHASE 3: SILVER IMPLEMENTATION (Functional Assistant)

Now that Bronze is validated, implement the Silver Tier requirements. Focus on adding external communication and the Human-in-the-Loop (HITL) safety layer.

1. WHATSAPP PERCEPTION:
   - Create `src/watchers/whatsapp_watcher.py` using Playwright.
   - It must monitor WhatsApp Web for keywords like 'urgent', 'invoice', or 'payment'.
   - When a match is found, create a .md file in `/Needs_Action`.

2. REASONING LOOP (Plan.md):
   - Upgrade the reasoning engine to generate a `Plan.md` file in the `/Plans` folder for every new task.
   - The plan must list checkboxes for each step and identify if an action requires approval.

3. ACTION LAYER (MCP & HITL):
   - Setup the `email-mcp` server to allow sending emails.
   - Implement the HITL logic: If an action is sensitive (like sending an email), create a file in `/Pending_Approval`.
   - The Orchestrator must only execute the action once the file is moved to `/Approved`.

4. AGENT SKILLS:
   - Create a new skill for 'LinkedIn Draft Generation' to create business posts in the vault.

5. SCHEDULING:
   - Provide the `cron` command for WSL to trigger a daily 'Social Media Check' at 9:00 AM.

STOP after generating the code for the WhatsApp Watcher and the HITL logic. Do not proceed to Gold tasks yet.

## Response snapshot

Implemented Silver Tier requirements including WhatsAppWatcher, email-mcp, HITL logic, and LinkedIn Draft skill.

## Outcome

- ✅ Impact: Functional Assistant capabilities added with HITL safety.
- 🧪 Tests: No automated tests run, manual validation required.
- 📁 Files: src/watchers/whatsapp_watcher.py, src/mcp/mcp_servers/email_mcp.py, src/reasoning/claude_interface.py, src/orchestrator.py, src/skills/agent_skills.py
- 🔁 Next prompts: Proceed to Gold Tier implementation.
- 🧠 Reflection: Layered architecture allowed for easy integration of new components.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Implement Gold Tier Odoo integration.
