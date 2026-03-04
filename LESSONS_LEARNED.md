# Lessons Learned: Building an Autonomous Digital FTE

## 1. The Power of "Agent Engineering" over "Prompt Engineering"
During this hackathon, we shifted from simply trying to get Claude to output the correct text to building a robust environment where Claude acts as the reasoning core of a larger system. The **Ralph Wiggum Stop Hook** pattern was transformative. By intercepting Claude's exit and enforcing a `--completion-promise`, we turned a reactive chatbot into an autonomous worker that iterates until a multi-step task is actually finished.

## 2. File-Based State Management is Resilient
Using Obsidian (Markdown files) as the central state machine proved incredibly effective. By passing data through `/Inbox`, `/Needs_Action`, `/Pending_Approval`, and `/Done`, we achieved:
* **Observability**: We can literally "see" what the AI is thinking and doing by watching files move.
* **Concurrency Control**: The Platinum Tier's `Claim-by-Move` rule prevented race conditions between the Cloud and Local agents simply by moving a file into an `/In_Progress/<agent>/` directory.
* **No Database Required**: We avoided complex database schemas and transaction locks, relying on the OS's atomic file move operations.

## 3. Playwright for "Computer Use" is Powerful but Brittle
Integrating WhatsApp and Social Media via Playwright headless browsers allowed us to bypass strict API limitations. However, we learned that:
* **User-Agents matter**: WhatsApp Web will reject outdated or default headless user agents. We had to explicitly set a modern Chrome on Windows string.
* **Viewport size**: Setting a realistic desktop viewport (`1280x800`) and disabling `is_mobile` was necessary to prevent web apps from serving simplified, selector-breaking mobile views.
* **Timing and Overlays**: We had to implement explicit wait times for "Syncing..." and "Loading..." overlays to disappear, and use `time.sleep` settling delays to ensure DOM elements were actually interactable.

## 4. Human-in-the-Loop (HITL) is Essential for Trust
Fully autonomous agents are dangerous when dealing with money or reputation. Implementing a strict `/Pending_Approval` gate for emails, social media posts, and Odoo invoices (especially those over $100) gave us the confidence to let the AI run wild on triage tasks while retaining ultimate veto power. 

## 5. The Hybrid Cloud-Local Split is the Future
The Platinum tier architecture—running a 24/7 "Cloud Agent" for email/social triage, and a secure "Local Agent" for executing payments and final approvals—provides the best of both worlds. 
* The Cloud Agent uses a draft-only Odoo integration and writes to `/Pending_Approval`.
* The Local Agent never syncs its `.env` or banking credentials to the cloud, ensuring high security while allowing continuous uptime.

## 6. System Stability Requires a Watchdog
Python scripts polling APIs indefinitely will eventually crash due to network blips. Writing `supervisor.py` to act as a watchdog process that wraps `main.py --loop` and auto-restarts it upon failure was necessary for true "production-ish" uptime.
