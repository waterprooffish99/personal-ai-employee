---
description: "Task list for Personal AI Employee System implementation"
---

# Tasks: Personal AI Employee System

**Input**: Design documents from `/specs/001-ai-employee-system/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/
- [x] T002 Initialize Python 3.13+ project with UV dependencies in pyproject.toml
- [ ] T003 [P] Configure linting and formatting tools in .pre-commit-config.yaml
- [x] T004 Create .env management system in src/utils/env_manager.py
- [x] T005 Set up DRY_RUN flag management in src/utils/dry_run.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create vault manager to handle file operations in src/vault/vault_manager.py
- [x] T007 [P] Create orchestrator.py as master process for logic glue
- [x] T008 [P] Create dashboard.md initialization in src/vault/vault_manager.py
- [x] T009 Create BaseWatcher abstract class in src/watchers/base_watcher.py
- [x] T010 Create vault directory structure (Inbox, Needs_Action, Plans, Done, Pending_Approval, Approved, Rejected, Logs, Briefings, Accounting)
- [x] T011 Create company_handbook.md with rules of engagement template

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - AI Employee Foundation (Priority: P1) 🎯 MVP

**Goal**: Create basic vault system with file monitoring and Claude Code integration to process tasks

**Independent Test**: Can initialize the vault, create required folder structure, and run a single watcher script that creates markdown files in the appropriate directories. The system should process a file dropped in the vault and generate a response in Dashboard.md.

### Implementation for User Story 1

- [x] T012 [P] [US1] Create FilesystemWatcher using watchdog in src/watchers/filesystem_watcher.py
- [x] T013 [US1] Create vault scaffolding with all required folders in src/vault/vault_manager.py
- [x] T014 [US1] Initialize Dashboard.md and Company_Handbook.md with core content
- [x] T015 [US1] Configure Claude Code integration to read tasks from /Needs_Action
- [x] T016 [US1] Implement logic to move processed files from /Needs_Action to /Done
- [x] T017 [US1] Create initial agent skills framework in src/skills/agent_skills.py
- [x] T018 [US1] Implement basic audit logging in JSON format to /Logs directory

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Multi-Watcher Assistant (Priority: P2)

**Goal**: Implement multiple watcher systems (Gmail and WhatsApp) and MCP action layer for sending communications

**Independent Test**: Can set up multiple watcher scripts simultaneously and verify they all create appropriate action files in the vault. The system should handle different communication channels and allow Claude to send emails via MCP only after human approval.

### Implementation for User Story 2

- [ ] T019 [P] [US2] Implement GmailWatcher to monitor unread important emails in src/watchers/gmail_watcher.py
- [ ] T020 [P] [US2] Implement WhatsAppWatcher using Playwright in src/watchers/whatsapp_watcher.py
- [ ] T021 [US2] Integrate email-mcp server for Claude to call MCP tools for external actions
- [ ] T022 [US2] Build HITL workflow logic where Claude writes sensitive requests to /Pending_Approval
- [ ] T023 [US2] Implement orchestrator logic to execute MCP action when file is moved to /Approved
- [ ] T024 [US2] Create skill for generating LinkedIn post drafts based on business activity

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Autonomous Business Intelligence (Priority: P3)

**Goal**: Implement Ralph Wiggum loop for autonomous task iteration, Odoo integration, and CEO Briefing generation

**Independent Test**: The system should run the Monday Morning CEO Briefing generation process and subscription audit logic. The Ralph Wiggum loop should allow Claude to iterate until tasks are confirmed complete.

### Implementation for User Story 3

- [ ] T025 [US3] Implement Ralph Wiggum Stop hook pattern for multi-step task iteration
- [ ] T026 [US3] Build Odoo MCP server to interface with Odoo Community via JSON-RPC in src/mcp/mcp_servers/odoo_mcp.py
- [ ] T027 [US3] Implement CEO Briefing weekly audit logic that reads transaction data and generates Monday_Morning_Briefing.md
- [ ] T028 [US3] Add with_retry decorator for exponential backoff and graceful degradation when APIs are unreachable
- [ ] T029 [US3] Create subscription audit logic to identify unused or duplicate software costs

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Cloud-Hybrid Executive (Priority: P4)

**Goal**: Deploy system for 24/7 operation with cloud VM, implement synchronization and concurrency control

**Independent Test**: The system should operate continuously on cloud VM while sensitive operations remain on local machine. Vault synchronization should work while excluding secrets.

### Implementation for User Story 4

- [ ] T030 [US4] Configure project for deployment on Cloud VM in deployment/ directory
- [ ] T031 [US4] Implement Git-based synchronization with secrets isolation for .env and tokens
- [ ] T032 [US4] Implement "claim-by-move" rule to prevent agents from duplicating work
- [ ] T033 [US4] Create watchdog.py to monitor PIDs and auto-restart failed watcher or orchestrator processes
- [ ] T034 [US4] Implement domain ownership logic (Cloud drafts emails; Local executes payments)

**Checkpoint**: All user stories should now be complete with cloud capabilities

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T035 [P] Documentation updates in README.md and docs/ directory
- [ ] T036 Code cleanup and refactoring across all modules
- [ ] T037 Performance optimization across all user stories
- [ ] T038 [P] Additional unit tests in tests/unit/ directory
- [ ] T039 Security hardening and validation of credential isolation
- [ ] T040 Run quickstart.md validation to ensure complete setup flow works
- [ ] T041 Create Business_Goals.md for tracking objectives
- [ ] T042 Implement cron/scheduler integration for automated tasks
- [ ] T043 Final verification that all actions create JSON logs in /Logs
- [ ] T044 Verify Dashboard.md is updated as single source of truth
- [ ] T045 Confirm payments >$100 are blocked by HITL as required

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority
- Each user story must be independently testable

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Create FilesystemWatcher using watchdog in src/watchers/filesystem_watcher.py"
Task: "Create vault scaffolding with all required folders in src/vault/vault_manager.py"
Task: "Initialize Dashboard.md and Company_Handbook.md with core content"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence