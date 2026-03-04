# Implementation Plan: Personal AI Employee System

**Branch**: `001-ai-employee-system` | **Date**: 2026-02-24 | **Spec**: specs/001-ai-employee-system/spec.md
**Input**: Feature specification from `/specs/001-ai-employee-system/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a local-first autonomous digital employee using a vault-based architecture with Claude Code reasoning engine. The system follows a progressive tier approach (Bronze → Silver → Gold → Platinum) starting with basic vault initialization and perception layer, then expanding to multi-channel monitoring, MCP integrations, business intelligence, and finally cloud hybrid operation. The architecture is modular with distinct layers: Perception (Watchers), Vault (State), Reasoning (Claude Code), Action (MCP Servers), and Orchestration.

## Technical Context

**Language/Version**: Python 3.13+ and Node.js v24+ LTS
**Primary Dependencies**: Claude Code terminal interface, Model Context Protocol (MCP) servers, Watchdog for file monitoring, Playwright for web automation, Obsidian API (for markdown-based interface)
**Storage**: File-based state management using Markdown files in Obsidian-compatible vault structure
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux/WSL (primary), with cloud VM deployment for Platinum tier
**Project Type**: Single project with layered architecture
**Performance Goals**: 99% uptime for Platinum tier, <30 minute setup time for Bronze tier, 90% of monitored inputs processed without human intervention
**Constraints**: DRY_RUN mode as default, zero credentials in version control, local-first data sovereignty, human approval required for sensitive actions (>$100 payments, new contacts, social DMs)
**Scale/Scope**: Single user operation with potential for enterprise expansion (future iteration)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Local-First Data Sovereignty**: All data remains under user control in local vault (PASS)
2. **File-Based State Management**: System state managed through Markdown files in vault (PASS)
3. **Modular Layered Architecture**: Clear separation of Perception, Vault, Reasoning, Action, and Orchestration layers (PASS)
4. **Human-in-the-Loop Safeguards**: Sensitive actions require human approval via /Pending_Approval workflow (PASS)
5. **Progressive Tier Enablement**: Implementation follows Bronze→Silver→Gold→Platinum roadmap (PASS)
6. **Security-First Implementation**: Secrets isolated in .env files, no credentials in vault or version control (PASS)
7. **Audit Requirements**: All actions logged in JSON format for audit trail (PASS)

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-employee-system/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── orchestrator.py             # Master process for logic glue
├── watchdog.py                 # Health monitor to restart failed scripts
├── watchers/
│   ├── __init__.py
│   ├── base_watcher.py         # BaseWatcher abstract class
│   ├── filesystem_watcher.py   # Monitor /Inbox directory
│   ├── gmail_watcher.py        # API-based email monitoring
│   └── whatsapp_watcher.py     # Playwright-based message monitoring
├── reasoning/
│   ├── __init__.py
│   └── claude_interface.py     # Claude Code integration
├── mcp/
│   ├── __init__.py
│   └── mcp_servers/
│       ├── email_mcp.py        # Email sending via MCP
│       ├── browser_mcp.py      # Web automation via MCP
│       ├── calendar_mcp.py     # Scheduling via MCP
│       └── odoo_mcp.py         # Accounting via MCP
├── vault/
│   ├── __init__.py
│   └── vault_manager.py        # Interface with Obsidian vault
├── utils/
│   ├── __init__.py
│   └── dry_run.py              # DRY_RUN flag management
└── skills/
    ├── __init__.py
    └── agent_skills.py         # Modular AI functionality
```

### Vault Structure
```text
AI_Employee_Vault/
├── Inbox/                    # Incoming tasks from Watchers
├── Needs_Action/            # Tasks for Claude to process
│   ├── Personal/            # Local-only sensitive tasks
│   └── Business/            # Cloud-triageable tasks
├── Plans/                   # Plan.md files generated by Claude
│   ├── Personal/
│   └── Business/
├── In_Progress/             # Claimed tasks (Platinum Rule)
│   ├── CloudAgent/
│   └── LocalAgent/
├── Done/                    # Completed task storage
├── Pending_Approval/        # HITL approval files
│   ├── Personal/
│   └── Business/
├── Approved/                # User-moved files to trigger action
├── Rejected/                # User-moved files to cancel action
├── Logs/                    # Audit trail in JSON format
├── Briefings/               # CEO Briefing outputs
├── Accounting/              # Odoo integration or .md ledgers
├── Signals/                 # Cloud -> Local dashboard update signals
├── Dashboard.md             # Real-time system GUI (Local Agent write-only)
└── Company_Handbook.md      # Rules of Engagement
```

**Structure Decision**: Single project with modular architecture following the constitutional requirement for layered separation of concerns. The structure supports the progressive tier approach with core components for Bronze tier expanding through Platinum tier. Vault structure follows constitutional requirements for file-based state management.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| MCP Servers | Required for Action Layer per constitution | Direct API calls would violate modular layered architecture |
