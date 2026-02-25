import os
import time
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
    This is a simplified version that simulates Claude interaction.
    """

    def __init__(self):
        """Initialize the Claude interface."""
        self.api_key = get_env("CLAUDE_API_KEY")
        self.active = True

    def process_needs_action_files(self):
        """
        Process all files in the Needs_Action directory.

        Returns:
            Number of files processed
        """
        needs_action_files = vault_manager.get_needs_action_files()
        processed_count = 0

        for file_path in needs_action_files:
            try:
                processed = self._process_single_file(file_path)
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
        Process a single file from Needs_Action.

        Args:
            file_path: Path to the file to process

        Returns:
            True if processed successfully, False otherwise
        """
        content = vault_manager.read_file(file_path)
        if content is None:
            log_action(
                f"Could not read file content: {file_path.name}",
                actor="AI",
                result="error",
                dry_run=is_dry_run()
            )
            return False

        # For now, simulate Claude processing by creating a simple response
        # In a real implementation, this would call the Claude API
        response_content = self._simulate_claude_response(content, file_path)

        # Update Dashboard.md with processing info
        self._update_dashboard(file_path.name)

        # Move the file to Done directory after processing
        success = vault_manager.move_to_done(file_path)

        if success:
            log_action(
                f"Claude processed file: {file_path.name}",
                actor="AI",
                result="success",
                details={"file_size": len(content)},
                dry_run=is_dry_run()
            )
            return True
        else:
            log_action(
                f"Failed to move processed file: {file_path.name}",
                actor="AI",
                result="error",
                dry_run=is_dry_run()
            )
            return False

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
        Update the Dashboard.md file with the latest information.

        Args:
            processed_item: Description of the item that was processed
        """
        try:
            # Get current stats from vault manager
            stats = vault_manager.get_vault_stats()

            # Update the dashboard
            vault_manager.create_initial_dashboard()

            log_action(
                "Dashboard updated after processing task",
                actor="AI",
                result="success",
                details={"processed_item": processed_item},
                dry_run=is_dry_run()
            )
        except Exception as e:
            log_action(
                "Failed to update dashboard",
                actor="AI",
                result="error",
                details={"error": str(e)},
                dry_run=is_dry_run()
            )

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