# Feature Specification: Personal AI Employee System

**Feature Branch**: `001-ai-employee-system`
**Created**: 2026-02-24
**Status**: Draft
**Input**: User description: "Functional Requirements by Tier: BRONZE REQUIREMENTS (Foundation): Vault Initialization, Folder Lifecycle, Perception, Reasoning Engine, Agent Skills, Safeguards; SILVER REQUIREMENTS (Functional Assistant): Multi-Watcher System, Reasoning Loop, MCP Integration, HITL Workflow, Business Growth, Scheduling; GOLD REQUIREMENTS (Autonomous Employee): Autonomous Persistence, Business Intelligence, Accounting Integration, Subscription Audit, Error Resilience; PLATINUM REQUIREMENTS (Always-On Executive): Hybrid Architecture, Concurrency Rules, Synchronization, Single-Writer Rule, Health Monitoring; Non-Functional & Security Requirements: Technical Stack Constraints, Security Boundaries; Deliverables: GitHub repository with production-grade structure, README, Security disclosure, Demo video"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - AI Employee Foundation (Priority: P1)

As a busy professional, I want to set up an AI employee that manages basic tasks in an Obsidian vault so that I can have a foundation for automated personal and business management.

**Why this priority**: This is the foundational tier that must be established before any advanced features can work. Without a working vault system and basic perception, the entire concept cannot function.

**Independent Test**: Can be fully tested by initializing the vault, creating the required folder structure, and running a single watcher script that creates markdown files in the appropriate directories. Delivers a working system where the AI can perceive and act on basic inputs.

**Acceptance Scenarios**:

1. **Given** user has installed the system, **When** vault is initialized, **Then** Dashboard.md and Company_Handbook.md are created with appropriate content
2. **Given** vault exists with folder structure, **When** a Gmail watcher detects an important email, **Then** an .md action file is created in the /Inbox directory
3. **Given** action files exist in /Inbox, **When** Claude processes them, **Then** they are moved to /Needs_Action with appropriate instructions
4. **Given** tasks in /Needs_Action, **When** Claude completes them, **Then** they are moved to /Done

---

### User Story 2 - Multi-Watcher Assistant (Priority: P2)

As a business owner, I want the AI employee to monitor multiple input sources (email, WhatsApp, files) so that it can handle various types of communications and tasks autonomously.

**Why this priority**: This expands the perception layer beyond basic functionality, enabling the AI to handle more diverse inputs and become a more useful assistant.

**Independent Test**: Can be fully tested by setting up multiple watcher scripts simultaneously and verifying they all create appropriate action files in the vault. Delivers a system that can handle different communication channels.

**Acceptance Scenarios**:

1. **Given** email and WhatsApp watchers are active, **When** important email is received, **Then** appropriate .md file is created in /Inbox
2. **Given** email and WhatsApp watchers are active, **When** WhatsApp message is received, **Then** appropriate .md file is created in /Inbox
3. **Given** multiple watchers active, **When** Claude processes action files, **Then** it can handle different types of tasks from different sources
4. **Given** email-mcp is integrated, **When** Claude needs to send email, **Then** it can do so through the MCP protocol

---

### User Story 3 - Autonomous Business Intelligence (Priority: P3)

As an executive, I want the AI employee to generate weekly business briefings and audit subscriptions so that I can make informed decisions and reduce costs automatically.

**Why this priority**: This provides high-value business intelligence that directly impacts the bottom line and justifies the AI employee investment.

**Independent Test**: Can be fully tested by running the Monday Morning CEO Briefing generation process and subscription audit logic. Delivers actionable insights and cost-saving recommendations.

**Acceptance Scenarios**:

1. **Given** business transactions are logged, **When** Sunday night arrives, **Then** CEO Briefing is generated with revenue, bottlenecks, and cost suggestions
2. **Given** financial data is available, **When** subscription audit runs, **Then** unused or duplicate software costs are flagged
3. **Given** task completion issues, **When** Ralph Wiggum loop is active, **Then** Claude iterates until tasks are confirmed complete
4. **Given** Odoo integration is configured, **When** accounting tasks are needed, **Then** they can be handled through the system

---

### User Story 4 - Cloud-Hybrid Executive (Priority: P4)

As a company executive, I want the AI employee to operate 24/7 with cloud hybrid architecture so that it can handle email and social media even when my local machine is offline.

**Why this priority**: This enables always-on operation, critical for business continuity and handling time-sensitive communications.

**Independent Test**: Can be fully tested by verifying cloud VM handles email triage and social drafts while sensitive banking/WhatsApp actions remain on local machine. Delivers continuous operation without compromising security.

**Acceptance Scenarios**:

1. **Given** cloud VM is deployed, **When** email arrives while local machine is offline, **Then** cloud handles initial triage
2. **Given** multiple agents might access same task, **When** claim-by-move rule is enforced, **Then** no duplicate work occurs
3. **Given** vault sync is configured, **When** Dashboard.md update is needed, **Then** only local machine can update it
4. **Given** Watcher or Orchestrator fails, **When** watchdog.py detects failure, **Then** the process is automatically restarted

---

### Edge Cases

- What happens when multiple watchers detect the same event simultaneously? The system must have concurrency rules to prevent duplicate action files.
- How does the system handle API rate limits from Gmail or bank services? The system must implement exponential backoff and queue management.
- What if Claude cannot complete a task after multiple iterations? The system must have a human review queue for complex failures.
- How does the system handle conflicts during Git synchronization? The system must resolve conflicts while maintaining data integrity.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST initialize an Obsidian-compatible vault with Dashboard.md and Company_Handbook.md
- **FR-002**: System MUST create folder lifecycle including /Inbox, /Needs_Action, and /Done directories
- **FR-003**: System MUST deploy at least one working Watcher script (Gmail or File System) to monitor inputs
- **FR-004**: System MUST configure Claude Code to read from and write to the vault using terminal-based tools
- **FR-005**: System MUST implement all AI functionality as modular "Agent Skills" rather than static prompts
- **FR-006**: System MUST enable DRY_RUN by default for all perception-to-action transitions
- **FR-007**: System MUST implement two or more Watchers, including a Playwright-based WhatsApp watcher
- **FR-008**: System MUST create Plan.md files where Claude outlines multi-step task execution
- **FR-009**: System MUST integrate at least one Model Context Protocol server for communications
- **FR-010**: System MUST establish /Pending_Approval to /Approved movement logic for sensitive actions
- **FR-011**: System MUST automate LinkedIn post drafts to generate sales leads
- **FR-012**: System MUST implement the "Ralph Wiggum" loop to allow Claude to iterate until tasks are confirmed complete
- **FR-013**: System MUST generate a "Monday Morning CEO Briefing" every Sunday night auditing revenue and bottlenecks
- **FR-014**: System MUST integrate Odoo Community via JSON-RPC APIs for business management
- **FR-015**: System MUST implement logic to flag unused or duplicate software costs based on transaction patterns
- **FR-016**: System MUST implement exponential backoff for transient API errors
- **FR-017**: System MUST deploy a cloud VM for 24/7 email triage while keeping sensitive actions on local machine
- **FR-018**: System MUST implement "claim-by-move" rule to prevent multiple agents from working on the same task
- **FR-019**: System MUST use Git or Syncthing for vault synchronization while excluding secrets
- **FR-020**: System MUST designate the Local machine as the sole authority for updating Dashboard.md
- **FR-021**: System MUST deploy watchdog.py to monitor and auto-restart failed scripts

### Key Entities

- **Vault**: The central storage system containing all business processes, tasks, and data in markdown files
- **Watcher**: Service components that monitor external inputs (email, WhatsApp, files, financial data) and create action files
- **Agent Skill**: Modular AI capabilities that can be reused across different tasks and scenarios
- **Plan.md**: Structured documents containing multi-step task execution instructions created by Claude
- **Dashboard.md**: Real-time system GUI providing status updates and executive summaries
- **Company_Handbook.md**: Rules of engagement and business processes defining how AI should operate
- **MCP Server**: Model Context Protocol servers that provide action capabilities to the AI reasoning engine
- **CEO Briefing**: Weekly business intelligence reports covering revenue, bottlenecks, and cost suggestions

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can initialize the AI employee system and have working vault with folder structure within 30 minutes of installation
- **SC-002**: System processes at least 90% of monitored inputs (emails, messages, files) without human intervention
- **SC-003**: Cost-per-task is reduced to under $0.50 compared to manual execution of similar tasks
- **SC-004**: System operates 24/7 with 99% uptime through cloud-hybrid architecture
- **SC-005**: 95% of business actions can be completed without human approval for known contacts/activities
- **SC-006**: CEO Briefings are generated weekly with actionable insights that lead to at least 2 cost-saving measures per month
- **SC-007**: Subscription audit identifies at least 1 unused or duplicate software cost per month
- **SC-008**: All sensitive actions maintain local-only processing with zero credentials committed to version control
- **SC-009**: System demonstrates clean audit trail for every AI-initiated payment or email
- **SC-010**: All system processes can be monitored and restarted through the watchdog mechanism with 99% reliability