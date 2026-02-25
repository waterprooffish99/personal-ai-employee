---
id: 2
title: Create AI Employee Plan
stage: plan
date: 2026-02-24
surface: agent
model: claude-opus-4-6
feature: 001-ai-employee-system
branch: 001-ai-employee-system
user: waterprooffish99
command: /sp.plan
labels: [planning, architecture, ai-employee, mcp, vault]
links:
  spec: specs/001-ai-employee-system/spec.md
  plan: specs/001-ai-employee-system/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-ai-employee-system/plan.md
 - specs/001-ai-employee-system/research.md
 - specs/001-ai-employee-system/data-model.md
 - specs/001-ai-employee-system/quickstart.md
 - specs/001-ai-employee-system/contracts/email-mcp.yaml
tests:
 - none
---

## Prompt

```
Phase 1: Foundation & Environment (The Nerve Center)

Initialize Environment: Set up a Python 3.13+ project using the uv package manager in WSL.


Vault Scaffolding: Initialize the AI_Employee_Vault with core files: Dashboard.md, Company_Handbook.md, and Business_Goals.md.
+1


Folder Structure: Create the state-management directories: /Needs_Action, /Plans, /Done, /Pending_Approval, /Approved, and /Logs.
+1


Security Baseline: Implement a .env management system and ensure a global DRY_RUN flag is active.

Phase 2: Bronze Implementation (The Foundation)

Perception (BaseWatcher): Develop the BaseWatcher abstract class and a FilesystemWatcher using watchdog to monitor /Inbox.
+1


Reasoning (Claude Code): Configure Claude Code to interact with the vault and read /Needs_Action files.
+1


Task Lifecycle: Implement the logic to move processed files from /Needs_Action to /Done upon completion.

M1 Milestone: Demonstrate a file being dropped into the vault and Claude generating a response in Dashboard.md.

Phase 3: Silver Expansion (The Functional Assistant)

Communication Senses: Implement the GmailWatcher (API-based) and WhatsAppWatcher (Playwright-based).
+1


Action Layer (MCP): Integrate the email-mcp server to allow Claude to send messages.


HITL Workflow: Build the "Human-in-the-Loop" bridge where sensitive actions are written to /Pending_Approval and only executed when moved to /Approved.
+1


Automation: Set up cron jobs for scheduled tasks like daily social media draft generation.
+2

Phase 4: Gold Expansion (The Autonomous Employee)

Persistence (Ralph Wiggum): Implement the "Ralph Wiggum" loop/Stop hook to allow Claude to continuously iterate on multi-step tasks without human prompting.
+2


Business Brain: Build the CEOBriefing generator to audit revenue and bottlenecks every Sunday night.
+1


Advanced Action: Integrate the Odoo Community (v19+) JSON-RPC MCP server for automated accounting.
+1


Error Recovery: Add the with_retry decorator for exponential backoff and graceful degradation if APIs are down.

Phase 5: Platinum Expansion (The Production Agent)

Cloud Orchestration: Deploy the "Perception Layer" (Watchers) to a Cloud VM (e.g., Oracle Free Tier) for 24/7 monitoring.


Vault Sync: Implement Git-based or Syncthing synchronization between the Cloud VM and the Local machine.


Delegation Model: Enforce the "claim-by-move" rule and "domain ownership" (Cloud drafts emails; Local executes payments).
+1


Watchdog Health: Deploy a watchdog.py process manager to ensure all daemons auto-restart after crashes or reboots.
+1

Milestones & Success Criteria
M1 (Bronze): Vault structure active; Claude reads a file and writes a log.


M2 (Silver): Claude sends an email via MCP only after local human approval.


M3 (Gold): Weekly CEO Briefing generated with revenue and bottleneck analysis.
+1


M4 (Platinum): End-to-end flow: Cloud detects email → drafts reply → Local user approves → Local executes send.
```

## Response snapshot

Created comprehensive implementation plan for the Personal AI Employee System with:

- Complete plan.md document with technical context, constitution check, and project structure
- Research.md with technology decisions and rationale
- Data-model.md with core entities, state transitions, and relationships
- Quickstart.md with installation and configuration instructions
- Sample API contract for email-mcp server

All artifacts align with constitutional requirements for local-first architecture, file-based state management, modular layered architecture, human-in-the-loop safeguards, and progressive tier enablement.

## Outcome

- ✅ Impact: Created complete planning artifacts for progressive tier implementation from Bronze to Platinum
- 🧪 Tests: none
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and contracts/email-mcp.yaml
- 🔁 Next prompts: Continue with task generation using /sp.tasks
- 🧠 Reflection: Plan provides clear roadmap for tiered implementation following constitutional principles

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Plan successfully created with all constitutional requirements validated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks using /sp.tasks command