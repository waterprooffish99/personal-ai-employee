<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.0.0
Modified principles:
- Local-First Privacy → Local-First Data Sovereignty
- File-Based State → File-Based State Management
- Modular Architecture → Modular Layered Architecture
- Human-in-the-Loop → Human-in-the-Loop Safeguards
- Progressive Tiers → Progressive Tier Enablement

Added sections: Security Principles, Architectural Layers
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending manual check
- README.md ⚠ pending manual check

Follow-up TODOs:
- Ratification date to be set to actual adoption date
-->

# personal-ai-employee Constitution

## Core Principles

### I. Local-First Data Sovereignty
All data, state, and business logic must remain under the user's complete control. Data never leaves the local environment without explicit permission. Obsidian-based GUI and vault system serves as the primary storage, ensuring user-owned infrastructure. This includes all personal information, credentials, and business processes.

### II. File-Based State Management
System state is managed through Markdown files and structured documents. File-based state provides transparency, version control, and human-readable persistence. All operations result in changes to local files that can be audited, versioned, and backed up using standard file system tools.

### III. Modular Layered Architecture
System follows a clear separation of concerns with distinct layers: Perception (Watchers), Vault (State), Reasoning (Claude Code), Action (MCP Servers), and Orchestration (Python scripts). Each layer has well-defined interfaces and can operate independently, allowing for modular development and maintenance.

### IV. Human-in-the-Loop Safeguards
All sensitive, irreversible, or high-value actions require explicit human approval. The system must pause and request approval for financial transactions, credential access, communication with new contacts, and any action that could have significant consequences. No autonomous execution without proper approval flow.

### V. Progressive Tier Enablement
Implementation follows a staged approach from Bronze to Platinum tier, with each tier building upon the previous. This ensures a working baseline before adding complexity. Features are incrementally added following the roadmap: Bronze (basic vault + 1 watcher) → Silver (multiple watchers + basic MCP) → Gold (advanced automation) → Platinum (cloud capabilities).

### VI. Security-First Implementation
Security and credential isolation are paramount. Secrets are never stored in the vault or version-controlled repositories. Credential rotation must be straightforward and regularly performed. All security practices must be followed before feature completion. Access patterns must be auditable and traceable.

## Architectural Standards

### Perception Layer Requirements
- BaseWatcher abstraction for all monitoring services
- Gmail watcher for important email monitoring via API
- WhatsApp watcher using Playwright for message monitoring
- File system watcher using Watchdog for Inbox monitoring
- Finance watcher for bank transaction logging

### Vault Layer Structure
- Standardized folder structure: /Needs_Action, /Plans, /Done, /Pending_Approval, /Approved, /Rejected, /Logs, /Briefings, /Accounting
- Dashboard.md as the primary human interface
- Company_Handbook.md for rules and processes
- Obsidian vault as the central storage system

### Action Layer Standards
- MCP (Model Context Protocol) servers for all external actions
- email-mcp for Gmail operations
- browser-mcp for web automation
- calendar-mcp for scheduling
- odoo-mcp for accounting integration

## Development Workflow

### Spec-Driven Development Process
All features must begin with a clear specification document before implementation. The process follows: Spec → Plan → Tasks → Implementation. Each stage must be validated before proceeding to the next. Requirements must be concrete and testable.

### Code Quality Standards
- Claude Code as the primary reasoning engine
- Agent Skills for reusable functionality
- Completion Promises for tracking task completion
- Ralph Wiggum Stop Hook for continuous iteration when needed

### Testing and Validation
- All changes must pass through the orchestrator.py master process
- Health monitoring via Watchdog.py for crash detection
- PM2 for process persistence
- Dry-run mode as default to prevent unintended side effects

## Security Principles

### Secret Isolation
Secrets and credentials must be isolated in .env files only, never stored in the vault or committed to version control. Secrets must never sync across systems. Monthly credential rotation required for API tokens.

### Permission Boundaries
Auto-approve known contacts and payees; Human-in-the-loop approval required for all new payees. Permission boundaries must be clearly defined and enforced.

### Audit Requirements
All AI-initiated payments and emails must have clean audit trails. Transaction logging required for financial operations. JSON format logs for all system operations.

## Governance

All development must adhere to the tier strategy: Bronze (Obsidian vault + Dashboard + 1 Watcher + Claude Code writing to vault) → Silver (Multiple Watchers + LinkedIn automation + MCP for email + Plan.md loop) → Gold (Odoo accounting + Weekly CEO Briefing + Audit logs + Ralph Wiggum autonomy) → Platinum (Cloud VM + Claim-by-move rule + Local/Cloud sync split).

Success criteria include: reduced cost-per-task (target ~$0.50), 24/7 autonomous operation without script crashes, zero credentials committed to version control, and clean audit trail for every AI-initiated action.

The constitution supersedes all other development practices. Any deviation must be documented and justified. All code reviews must verify constitution compliance.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2026-02-24
