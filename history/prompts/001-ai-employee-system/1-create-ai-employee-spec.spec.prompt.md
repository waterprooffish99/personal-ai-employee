---
id: 1
title: Create AI Employee Spec
stage: spec
date: 2026-02-24
surface: agent
model: claude-opus-4-6
feature: 001-ai-employee-system
branch: 001-ai-employee-system
user: waterprooffish99
command: /sp.specify
labels: [specification, ai-employee, requirements, vault]
links:
  spec: specs/001-ai-employee-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-ai-employee-system/spec.md
 - specs/001-ai-employee-system/checklists/requirements.md
tests:
 - none
---

## Prompt

```
/sp.specify
Functional Requirements by Tier
BRONZE REQUIREMENTS (Foundation)


Vault Initialization: Create an Obsidian-compatible vault including Dashboard.md for real-time summaries and Company_Handbook.md for rules of engagement.


Folder Lifecycle: Implement /Inbox, /Needs_Action, and /Done directories to manage task states.


Perception: Deploy one working Watcher script (Gmail or File System) to monitor inputs and create .md action files.
+1


Reasoning Engine: Configure Claude Code to read from and write to the vault using terminal-based tools.
+1


Agent Skills: Implement all AI functionality as modular "Agent Skills" rather than static prompts.


Safeguards: Enable DRY_RUN by default for all perception-to-action transitions.
+1

SILVER REQUIREMENTS (Functional Assistant)


Multi-Watcher System: Implement two or more Watchers, including a Playwright-based WhatsApp watcher.
+1


Reasoning Loop: Implement the creation of Plan.md files where Claude outlines multi-step task execution.
+1


MCP Integration: Integrate at least one Model Context Protocol server, specifically email-mcp for sending communications.
+1


HITL Workflow: Establish the /Pending_Approval to /Approved movement logic for sensitive actions.


Business Growth: Automate LinkedIn post drafts to generate sales leads.


Scheduling: Implement automated triggers via cron or Task Scheduler.

GOLD REQUIREMENTS (Autonomous Employee)


Autonomous Persistence: Implement the "Ralph Wiggum" loop (Stop hook) to allow Claude to iterate until tasks are confirmed complete.
+2


Business Intelligence: Generate a "Monday Morning CEO Briefing" every Sunday night auditing revenue, bottlenecks, and proactive cost suggestions.
+1


Accounting Integration: Integrate Odoo Community (v19+) via JSON-RPC APIs for local business management.


Subscription Audit: Implement logic to flag unused or duplicate software costs based on transaction patterns.
+1


Error Resilience: Implement exponential backoff for transient API errors and a human review queue for logic failures.

PLATINUM REQUIREMENTS (Always-On Executive)


Hybrid Architecture: Deploy a Cloud VM for 24/7 email triage and social drafts, while keeping sensitive banking/WhatsApp actions on the Local machine.


Concurrency Rules: Implement the "claim-by-move" rule to prevent multiple agents from working on the same task.


Synchronization: Utilize Git or Syncthing for vault synchronization while strictly excluding secrets (.env, tokens) from sync.
+1


Single-Writer Rule: Designate the Local machine as the sole authority for updating Dashboard.md.


Health Monitoring: Deploy a watchdog.py process to monitor and auto-restart failed Watcher or Orchestrator scripts.
+1

Non-Functional & Security Requirements
Technical Stack Constraints


Runtime: Python 3.13+ and Node.js v24+ LTS.


Package Management: Use UV for Python project orchestration.


Hardware: Minimum 8GB RAM and 4-core CPU.


Logging: Retain audit logs in /Vault/Logs/ for a minimum of 90 days.

Security Boundaries


Credential Management: Secrets must never be stored in the vault; use environment variables or dedicated managers.


Permission Thresholds: Always require manual approval for payments >$100, new email recipients, or social media DMs.
+1


Audit Trail: Every action must log a JSON object containing the timestamp, actor, action type, and approval status.

Deliverables

GitHub repository with a production-grade structure.

README including setup instructions and a tier declaration.

Security disclosure regarding credential handling.

5-10 minute demo video showcasing an end-to-end task flow.
```

## Response snapshot

Created the complete specification for the Personal AI Employee System at specs/001-ai-employee-system/spec.md, including:

- User scenarios for each tier (Foundation, Functional Assistant, Autonomous Employee, Always-On Executive)
- 21 functional requirements covering all aspects from vault initialization to cloud hybrid operation
- Key entities definition including Vault, Watcher, Agent Skills, Plan.md, Dashboard.md, etc.
- 10 measurable success outcomes with specific metrics
- Edge cases for concurrency, API rate limits, task failures, and synchronization conflicts

Also created a specification quality checklist at specs/001-ai-employee-system/checklists/requirements.md to validate the completeness of the spec.

## Outcome

- ✅ Impact: Created comprehensive specification for the Personal AI Employee System with all requirements across all tiers
- 🧪 Tests: none
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Continue with planning using /sp.plan or clarifying with /sp.clarify
- 🧠 Reflection: Specification captures the full vision of the progressive tier system from Bronze to Platinum

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Specification successfully created with all required elements
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature planning using /sp.plan