---
id: 3
title: Create AI Employee Tasks
stage: tasks
date: 2026-02-24
surface: agent
model: claude-opus-4-6
feature: 001-ai-employee-system
branch: 001-ai-employee-system
user: waterprooffish99
command: /sp.tasks
labels: [tasks, planning, ai-employee, implementation]
links:
  spec: specs/001-ai-employee-system/spec.md
  plan: specs/001-ai-employee-system/plan.md
  tasks: specs/001-ai-employee-system/tasks.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-ai-employee-system/tasks.md
 - specs/001-ai-employee-system/spec.md
tests:
 - none
---

## Prompt

```
/sp.tasks
Phase 1: Project Scaffolding & Bronze Foundation
[ ] Initialize Environment: Set up the UV project with Python 3.13+ and Node.js v24+. Configure a .env management system and a global DRY_RUN flag.
+2

[ ] Vault Scaffold: Create the AI_Employee_Vault with core folders: /Needs_Action, /Plans, /Done, /Pending_Approval, /Approved, /Rejected, /Logs, /Briefings, and /Accounting.

[ ] Core Documentation: Initialize Dashboard.md for status summaries , Company_Handbook.md for rules of engagement , and Business_Goals.md for tracking objectives.
+3

[ ] Base Perception: Implement the BaseWatcher abstract class and a FilesystemWatcher using watchdog to monitor local file drops and create .md action files.
+1

[ ] Reasoning Integration: Configure Claude Code to read tasks from /Needs_Action and write initial responses to Dashboard.md.

Phase 2: Silver - Comms & Action Layer
[ ] Gmail Perception: Implement GmailWatcher to monitor unread important emails and generate action files in the vault.
+1

[ ] WhatsApp Perception: Implement WhatsAppWatcher using Playwright automation to monitor keywords like "urgent" or "invoice".
+1

[ ] MCP Action Layer: Integrate the email-mcp server. Develop an abstraction to allow Claude to call MCP tools for external actions.
+1

[ ] HITL Workflow: Build the logic where Claude writes sensitive requests to /Pending_Approval. The orchestrator must only execute the MCP action when the file is moved to /Approved.
+2

[ ] Social Drafts: Create a skill for generating LinkedIn post drafts based on business activity.

Phase 3: Gold - Business Intelligence & Persistence
[ ] Ralph Wiggum Loop: Implement the Stop hook pattern to allow Claude to iterate autonomously on multi-step tasks until a TASK_COMPLETE promise is met.
+2

[ ] Odoo Integration: Build an MCP server to interface with Odoo Community (v19+) via JSON-RPC for automated accounting.
+1

[ ] CEO Briefing: Implement the weekly audit logic that reads Bank_Transactions.md, identifies subscription patterns, and generates a Monday_Morning_Briefing.md.
+2

[ ] Resilience Layer: Add the with_retry decorator for exponential backoff and logic for graceful degradation when APIs are unreachable.

Phase 4: Platinum - Cloud & Synchronization
[ ] Cloud Orchestration: Configure the project for deployment on a Cloud VM (e.g., Oracle/AWS) for 24/7 "always-on" watchers.

[ ] Vault Sync: Implement Git-based synchronization. Enforce the "secrets isolation" rule to ensure .env and tokens never sync between cloud and local.
+1

[ ] Concurrency Control: Implement the "claim-by-move" rule to prevent agents from duplicating work.
+1

[ ] Health Watchdog: Implement watchdog.py to monitor PIDs and auto-restart failed watcher or orchestrator processes.
+1

Final Verification Checklist
[ ] Does every action create a JSON log in /Logs?

[ ] Is the Dashboard.md updated as the single source of truth?

[ ] Are payments >$100 strictly blocked by HITL?
+1
```

## Response snapshot

Created comprehensive task list for the Personal AI Employee System with:

- 42 specific tasks organized by priority and user story
- Setup phase (T001-T005) for environment initialization
- Foundational phase (T006-T011) for core infrastructure
- User Story 1 (T012-T018) for Bronze tier foundation
- User Story 2 (T019-T024) for Silver tier multi-watcher functionality
- User Story 3 (T025-T029) for Gold tier business intelligence
- User Story 4 (T030-T034) for Platinum tier cloud capabilities
- Polish phase (T035-T045) for final verification and cross-cutting concerns

All tasks follow the required format with task IDs, story labels where appropriate, and specific file paths. The tasks enable independent implementation and testing of each user story while maintaining proper dependencies.

## Outcome

- ✅ Impact: Created complete task breakdown for progressive tier implementation from Bronze to Platinum
- 🧪 Tests: none
- 📁 Files: Created tasks.md with 42 specific implementation tasks
- 🔁 Next prompts: Begin implementation using the generated tasks
- 🧠 Reflection: Tasks organized by user story enable parallel development and independent delivery

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Tasks successfully created with proper format and dependencies
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation of T001-T005 setup tasks