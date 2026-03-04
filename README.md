# 🤖 Personal AI Employee: The Digital FTE (2026)
> [cite_start]**Your life and business on autopilot.** Local-first, agent-driven, human-in-the-loop[cite: 1, 2].

[![Tier: Platinum](https://img.shields.io/badge/Tier-Platinum-blueviolet.svg)](#-evolution-tiers)
[![Framework: Claude Code](https://img.shields.io/badge/Framework-Claude_Code-orange.svg)](#-tech-stack)
[![Security: HITL Verified](https://img.shields.io/badge/Security-HITL_Verified-green.svg)](#-safety--security)

[cite_start]This project is a comprehensive architectural implementation of a **Digital FTE** (Full-Time Equivalent)—an autonomous AI agent that is built, "hired," and priced like a human employee[cite: 19]. [cite_start]It proactively manages personal and business affairs 24/7 using a futuristic, local-first approach[cite: 3].

---

## 📊 Human FTE vs. Digital FTE
[cite_start]*Based on 2026 industry benchmarks included in the system's reasoning engine[cite: 21, 22, 23]:*

| Feature | Human FTE | Digital FTE (This Agent) |
| :--- | :--- | :--- |
| **Availability** | 40 hours / week | [cite_start]**168 hours / week (24/7)** [cite: 21] |
| **Consistency** | Variable (85–95%) | [cite_start]**Predictable (99%+)** [cite: 21] |
| **Cost per Task** | ~$3.00 – $6.00 | [cite_start]**~$0.25 – $0.50** [cite: 21] |
| **Annual Hours** | ~2,000 hours | [cite_start]**~8,760 hours** [cite: 21] |
| **Aha! Moment** | Standard Labor | [cite_start]**85–90% Cost Reduction** [cite: 23] |

---

## 🏗️ System Architecture: Perception → Reasoning → Action
[cite_start]The system follows a modular "Sense-Think-Act" loop to solve complex problems without manual prompting[cite: 45].

### 🧠 The Brain (Reasoning)
[cite_start]Powered by **Claude Code**, utilizing the **Ralph Wiggum Stop Hook** pattern[cite: 10, 11]. [cite_start]This allows the agent to continuously iterate on multi-step tasks until a "TASK_COMPLETE" promise is fulfilled[cite: 74, 76].

### 💾 The Memory & GUI (Obsidian)
[cite_start]A local-first Markdown vault serves as the agent's long-term memory and your management dashboard[cite: 12, 39, 95].
* [cite_start]**Dashboard.md**: Real-time summary of bank balances, pending tasks, and active projects[cite: 40].
* [cite_start]**Company_Handbook.md**: The "Rules of Engagement" (e.g., "Always be polite," "Flag payments >$500")[cite: 41].

### 👁️ The Senses (Watchers)
[cite_start]Lightweight Python "Sentinel" scripts monitor inputs 24/7 to trigger the AI[cite: 13, 15, 48]:
* [cite_start]**Gmail Watcher**: Monitors important, unread emails[cite: 53].
* **WhatsApp Watcher**: Playwright-based automation for urgent client messages[cite: 57, 58].
* [cite_start]**Social Media Watcher**: Tracks mentions and DMs across FB, Instagram, and Twitter (X)[cite: 29].
* [cite_start]**Finance Watcher**: Logs new bank transactions for automated accounting[cite: 46].

### 🦾 The Hands (Action Layer)
[cite_start]Utilizes **Model Context Protocol (MCP)** servers to interact with the world[cite: 14, 65]:
* [cite_start]**Odoo MCP**: Full integration with Odoo Community (v19+) via JSON-RPC for invoicing and accounting[cite: 28, 110].
* **Social MCP**: Autonomous posting and summary generation for social platforms[cite: 29].
* [cite_start]**Email/Browser MCP**: Sending communications and interacting with payment portals[cite: 67, 71].

---

## 💎 Platinum Tier: Hybrid Cloud-Local Deployment
[cite_start]The system is deployed in a high-security **Split-Ownership** model[cite: 29, 31]:
* **Cloud Agent (24/7)**: Lives on a Cloud VM (Oracle/AWS). It handles email triage, social media drafts, and accounting prep[cite: 30, 31].
* **Local Agent (Secure)**: Lives on your local machine. [cite_start]It holds the keys to WhatsApp sessions, banking credentials, and final "Post/Send" actions[cite: 31, 35].
* [cite_start]**Claim-by-Move**: Agents use an atomic rule—the first agent to move a task from `/Needs_Action` to `/In_Progress/<agent>/` owns it, preventing double-work[cite: 33].
* **Secure Sync**: A Git-based sync ensures state is shared, but secrets (`.env`, tokens, credentials) never leave your local machine[cite: 32, 34].

---

## 📈 Key Business Features
### 📅 Monday Morning CEO Briefing
Every week, the agent audits `Business_Goals.md`, `Bank_Transactions.md`, and completed tasks to generate a high-level briefing[cite: 81, 82]. It reports **MTD Revenue**, identifies **Bottlenecks**, and makes **Proactive Suggestions** (e.g., "Cancel this unused $15/mo subscription")[cite: 91, 94].

### 🛡️ Safety & HITL (Human-in-the-Loop)
The agent is strictly forbidden from irreversible actions without approval[cite: 157].
1. Claude detects a sensitive action (e.g., a $500 payment)[cite: 72].
2. It writes an approval request to `/Pending_Approval/`[cite: 72].
3. The action remains paused until you move the file to `/Approved/`[cite: 72].

---

## 🛠️ Installation & Setup
1. **Prerequisites**: Python 3.13+, Node.js v24+, Obsidian, and Claude Code[cite: 25].
2. **Setup**:
   ```bash
   # Install Claude Code
   npm install -g @anthropic/claude-code
   
   # Clone and setup UV Python project
   git clone <repo-url>
   cd personal-ai-employee

   Execution:

Local: python3 supervisor.py --role Local

Cloud: python3 supervisor.py --role Cloud

Developed by Salman (Waterproof Fish) as part of the Personal AI Employee Hackathon 0, 2026.