# Quickstart Guide: Personal AI Employee System

**Date**: 2026-02-24
**Feature**: 001-ai-employee-system
**Status**: Complete

## Overview

This guide will help you set up the Personal AI Employee System quickly. The system follows a progressive tier approach, starting with Bronze (foundational) features and expanding to Platinum (cloud-enabled) features.

## Prerequisites

- **System**: WSL on Windows, Ubuntu (as specified in requirements)
- **Runtime**: Python 3.13+ and Node.js v24+ LTS
- **Package Manager**: UV for Python project orchestration
- **Hardware**: Minimum 8GB RAM and 4-core CPU
- **Access**: Claude Code terminal access
- **Vault**: Obsidian installation (optional but recommended for GUI)

## Installation Steps

### 1. Environment Setup

```bash
# Install Python 3.13+ if not already installed
# Install Node.js v24+ LTS if not already installed

# Install UV package manager
pip install uv

# Clone the repository
git clone <repository-url>
cd personal-ai-employee

# Install project dependencies using UV
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 2. Vault Initialization

```bash
# Run the initialization script
python -m src.vault.vault_manager init

# This creates the vault structure:
# - Dashboard.md (real-time system GUI)
# - Company_Handbook.md (rules of engagement)
# - Business_Goals.md
# - /Inbox, /Needs_Action, /Plans, /Done, /Pending_Approval, /Approved, /Logs directories
```

### 3. Environment Configuration

```bash
# Create .env file for secrets (NEVER commit to version control)
cp .env.example .env

# Edit .env file with your credentials
# - Claude API key
# - Gmail API credentials (for Silver tier)
# - WhatsApp credentials (for Silver tier)
# - Odoo credentials (for Gold tier)

# Ensure DRY_RUN is enabled by default
echo "DRY_RUN=true" >> .env
```

### 4. First Run

```bash
# Start the orchestrator (main process)
python src/orchestrator.py

# Or for development, start individual components:
# Start the Base Watcher
python -m src.watchers.filesystem_watcher
```

## Bronze Tier Activation

After installation, your system includes:

### Vault Structure
- ✅ Dashboard.md created with real-time summary capabilities
- ✅ Company_Handbook.md created with rules of engagement
- ✅ Required directories: /Inbox, /Needs_Action, /Plans, /Done, /Pending_Approval, /Approved, /Logs
- ✅ Security baseline with DRY_RUN flag active by default

### Perception Layer
- ✅ BaseWatcher abstract class implemented
- ✅ FilesystemWatcher monitoring /Inbox with watchdog
- ✅ New files in /Inbox trigger Claude processing

### Reasoning Layer
- ✅ Claude Code configured to read /Needs_Action files
- ✅ Task lifecycle implemented (moves processed files to /Done)

### M1 Milestone Check
1. Drop a test file into the /Inbox directory
2. Claude should process the file and create a response in Dashboard.md
3. Check the /Logs directory for audit trail in JSON format

## Configuration for Higher Tiers

### Silver Tier Setup (After Bronze Validation)

1. **Gmail Integration**:
   - Configure Gmail API credentials in .env
   - Enable GmailWatcher in orchestrator

2. **WhatsApp Integration**:
   - Install Playwright: `uv pip install playwright`
   - Run `playwright install` for browser dependencies
   - Configure WhatsApp credentials in .env

3. **MCP Integration**:
   - Set up email-mcp server for Claude to send messages
   - Configure HITL workflow for sensitive actions

### Running the System

```bash
# Development mode (with auto-restart)
python src/orchestrator.py --dev

# Production mode
python src/orchestrator.py --production

# With specific tier level
python src/orchestrator.py --tier bronze
python src/orchestrator.py --tier silver
python src/orchestrator.py --tier gold
python src/orchestrator.py --tier platinum
```

## Verification Steps

### Bronze Tier Verification:
1. **Vault Check**: Verify all directories are created and accessible
2. **Watcher Check**: Drop a test file in /Inbox and verify it moves to /Needs_Action
3. **Claude Check**: Verify Claude processes files and moves them to /Done
4. **Security Check**: Confirm DRY_RUN is enabled by default
5. **Audit Check**: Verify JSON logs are created in /Logs directory

### M1 Milestone Test:
1. Create a simple test file in /Inbox: `echo "Hello" > AI_Employee_Vault/Inbox/test.md`
2. Wait for Claude to process it
3. Check Dashboard.md for response
4. Check /Logs for audit entry

## Troubleshooting

- **Vault not initializing**: Ensure .env file is properly configured
- **Claude not responding**: Check Claude terminal access and API keys
- **Watchers not monitoring**: Ensure watchdog is properly installed via UV
- **DRY_RUN not working**: Verify DRY_RUN=true in .env file
- **Permission errors**: Check file permissions on vault directory

## Next Steps

Once Bronze tier is confirmed working:

1. Move to Silver Tier by adding Gmail and WhatsApp watchers
2. Implement MCP integration for email sending
3. Set up HITL workflow for sensitive actions
4. Configure cron jobs for scheduled tasks
5. Progress to Gold and Platinum tiers as needed