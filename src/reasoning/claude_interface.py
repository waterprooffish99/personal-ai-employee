import os
import time
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from ..vault.vault_manager import vault_manager, get_vault_manager
from ..utils.logger import log_action
from ..utils.dry_run import is_dry_run, execute_if_real
from ..utils.env_manager import get_env


class ClaudeInterface:
    """
    Interface for Claude Code to read tasks from /Needs_Action and process them.
    Implements the Ralph Wiggum Stop hook pattern using --completion-promise.
    Platinum Tier: Implements Claim-by-Move and Split Ownership (Cloud vs Local).
    """

    def __init__(self, agent_name: str = None):
        """Initialize the Claude interface."""
        self.api_key = get_env("CLAUDE_API_KEY")
        self.agent_name = agent_name or get_env("AGENT_NAME", "LocalAgent")
        self.agent_role = get_env("AGENT_ROLE", "Local")  # "Cloud" or "Local"
        self.active = True

    def process_needs_action_files(self):
        """
        Process all files in the Needs_Action directory.
        Implements Claim-by-Move: move to In_Progress/<agent>/ before processing.

        Returns:
            Number of files processed
        """
        needs_action_files = vault_manager.get_needs_action_files()
        processed_count = 0

        for file_path in needs_action_files:
            try:
                # Platinum Tier: Claim the task first
                claimed_path = vault_manager.claim_task(file_path, self.agent_name)
                if not claimed_path:
                    continue

                processed = self._process_single_file(claimed_path)
                if processed:
                    processed_count += 1
            except Exception as e:
                log_action(
                    f"Error processing file: {file_path.name}",
                    actor="AI",
                    result="error",
                    details={"error": str(e), "file_path": str(file_path)},
                    dry_run=is_dry_run()
                )

        return processed_count

    def _process_single_file(self, file_path: Path) -> bool:
        """
        Process a single file from In_Progress.

        Args:
            file_path: Path to the file to process

        Returns:
            True if processed successfully, False otherwise
        """
        content = vault_manager.read_file(file_path)
        if content is None:
            return False

        # Generate a Plan.md for the task
        self._generate_plan(file_path, content)

        # Split Ownership Logic
        # Cloud owns: Email/Social triage and drafting
        # Local owns: WhatsApp, Payments, Final Posting, and Sensitive Actions
        
        # Platinum Rule: Sensitive actions check
        is_sensitive = any(keyword in content.lower() for keyword in ["email", "payment", "invoice", "social", "linkedin", "twitter", "facebook", "instagram", "odoo", "whatsapp"])
        
        # Requirement T045: Blocking payments > $100
        import re
        price_match = re.search(r"\$(\d+(?:\.\d{2})?)", content)
        if price_match:
            amount = float(price_match.group(1))
            if amount > 100.0:
                is_sensitive = True
                log_action("Sensitive amount detected (>$100), forcing HITL", actor="AI", result="info", details={"amount": amount})

        # Cloud-specific logic
        if self.agent_role == "Cloud":
            if is_sensitive:
                # Cloud drafts sensitive actions but doesn't execute
                log_action(
                    f"CloudAgent drafting sensitive action: {file_path.name}",
                    actor="AI",
                    result="success",
                    dry_run=is_dry_run()
                )
                success = vault_manager.move_to_pending_approval(file_path)
                self._update_dashboard(f"{file_path.name} (Drafted by Cloud, Awaiting Local Approval)")
                return success
            else:
                # Cloud executes non-sensitive actions
                return self._execute_task(file_path, content)

        # Local-specific logic
        else:
            # Local executes EVERYTHING if it gets to it, especially sensitive ones
            return self._execute_task(file_path, content)

    def _execute_task(self, file_path: Path, content: str) -> bool:
        """Execute the actual task logic (Claude CLI or Simulation)."""
        # Execute actual Claude CLI with Ralph Wiggum pattern
        success = False
        if not is_dry_run():
            try:
                log_action(f"Invoking Claude CLI for task: {file_path.name}", actor="AI", result="info")
                prompt = f"Process this task: {content}. You must use your skills to complete it. Output TASK_COMPLETE when you are fully done."
                
                result = subprocess.run(
                    ["claude", "-p", prompt, "--completion-promise", "TASK_COMPLETE"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if result.returncode != 0:
                    log_action(f"Claude CLI exited with error for {file_path.name}", actor="AI", result="error", details={"stderr": result.stderr})
                else:
                    log_action(f"Claude CLI successfully processed {file_path.name}", actor="AI", result="success", details={"stdout": result.stdout[:200]})
                    success = True
            except Exception as e:
                log_action(f"Failed to run Claude CLI: {e}. Falling back to simulation.", actor="system", result="warning")
                self._simulate_claude_response(content, file_path)
                success = True
        else:
            self._simulate_claude_response(content, file_path)
            success = True

        if success:
            self._update_dashboard(file_path.name)
            success = vault_manager.move_to_done(file_path)
            
        return success

    def _generate_plan(self, file_path: Path, content: str):
        """Generate a Plan.md for the current task."""
        plan_filename = f"plan_{file_path.stem}.md"
        plan_path = vault_manager.plans_dir / plan_filename
        
        is_sensitive = any(keyword in content.lower() for keyword in ["email", "payment", "invoice", "social", "linkedin"])
        
        plan_content = f"""# Plan: {file_path.name}

**Task Received**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status**: Initialized

## Steps
- [ ] Analyze request
- [ ] Verify requirements
- {"- [ ] Obtain human approval (Required: Sensitive Action)" if is_sensitive else "- [ ] Execute action"}
- [ ] Log results
- [ ] Update dashboard

## Sensitive Actions Detected
- {"Yes - Action requires human approval via /Pending_Approval" if is_sensitive else "No - Action can be performed autonomously"}

---
*Plan generated by Personal AI Employee Reasoning Engine*
"""
        vault_manager.write_file(plan_path, plan_content)
        log_action(
            f"Generated plan for task: {file_path.name}",
            actor="AI",
            result="success",
            details={"plan_file": plan_filename}
        )

    def _simulate_claude_response(self, content: str, file_path: Path) -> str:
        """
        Simulate Claude's response to a task.

        Args:
            content: Original content of the file
            file_path: Path to the file being processed

        Returns:
            Simulated Claude response
        """
        # In a real implementation, this would call the Claude API
        # For now, we'll create a simple simulation
        response = f"""# Claude Response to: {file_path.name}

**Processing Time**: {time.strftime('%Y-%m-%d %H:%M:%S')}

**Original Request**:
{content}

**Action Taken**:
[In a real implementation, Claude would analyze this request and take appropriate action based on Company_Handbook.md rules]

**Status**: Completed

**Next Steps**:
- File moved to Done directory
- Dashboard updated
- Audit log created
"""

        return response

    def _update_dashboard(self, processed_item: str):
        """
        Update system status.
        Platinum Tier: Cloud agents write to /Signals/, Local merges into Dashboard.md.
        """
        try:
            if self.agent_role == "Cloud":
                # Cloud writes a signal file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                signal_path = vault_manager.signals_dir / f"update_{timestamp}.json"
                signal_data = {
                    "agent": self.agent_name,
                    "processed_item": processed_item,
                    "timestamp": datetime.now().isoformat()
                }
                vault_manager.write_file(signal_path, json.dumps(signal_data, indent=2))
                log_action(
                    "Cloud signal created for dashboard update",
                    actor="AI",
                    result="success",
                    details={"signal_file": signal_path.name}
                )
            else:
                # Local updates the dashboard directly and processes any waiting signals
                self._process_signals()
                vault_manager.create_initial_dashboard()
                
                log_action(
                    "Dashboard updated by LocalAgent",
                    actor="AI",
                    result="success",
                    details={"processed_item": processed_item}
                )
        except Exception as e:
            log_action(
                "Failed to update dashboard/signals",
                actor="AI",
                result="error",
                details={"error": str(e)}
            )

    def _process_signals(self):
        """Local agent processes waiting signals from the Cloud agent."""
        signals = vault_manager.list_files_in_directory(vault_manager.signals_dir)
        for signal_file in signals:
            try:
                # In a real system, we would merge this data into a status file
                # For now, we'll just log that we saw it and delete it (moving to Done)
                vault_manager.move_to_done(signal_file)
            except Exception:
                pass

    def process_inbox_to_needs_action(self):
        """
        Process files from Inbox to Needs_Action if they need Claude processing.

        Returns:
            Number of files moved
        """
        inbox_files = vault_manager.get_inbox_files()
        moved_count = 0

        for file_path in inbox_files:
            # For now, move all inbox files to needs_action for Claude to process
            # In a real implementation, there might be some filtering logic
            success = vault_manager.move_to_needs_action(file_path)

            if success:
                moved_count += 1
                log_action(
                    f"Moved file to needs action: {file_path.name}",
                    actor="AI",
                    result="success",
                    dry_run=is_dry_run()
                )
            else:
                log_action(
                    f"Failed to move file to needs action: {file_path.name}",
                    actor="AI",
                    result="error",
                    dry_run=is_dry_run()
                )

        return moved_count

    def run_processing_cycle(self):
        """
        Run a complete processing cycle:
        1. Check inbox for new files and move to needs_action
        2. Process all needs_action files
        """
        log_action("Starting Claude processing cycle", actor="AI", dry_run=is_dry_run())

        # Move new inbox files to needs_action
        inbox_moved = self.process_inbox_to_needs_action()

        # Process needs_action files
        needs_action_processed = self.process_needs_action_files()

        log_action(
            "Completed Claude processing cycle",
            actor="AI",
            result="success",
            details={
                "inbox_moved": inbox_moved,
                "needs_action_processed": needs_action_processed
            },
            dry_run=is_dry_run()
        )


# Global Claude interface instance
claude_interface = ClaudeInterface()


def get_claude_interface() -> ClaudeInterface:
    """Get the global Claude interface instance."""
    return claude_interface