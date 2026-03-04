import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
from datetime import datetime

from ..utils.env_manager import get_env
from ..utils.dry_run import is_dry_run, execute_if_real
from ..utils.logger import log_action


class VaultManager:
    """Manages file operations for the AI Employee vault."""

    def __init__(self, vault_path: str = None):
        """
        Initialize the vault manager.

        Args:
            vault_path: Path to the vault directory (defaults to VAULT_PATH env var)
        """
        if vault_path is None:
            self.vault_path = Path(get_env("VAULT_PATH", "AI_Employee_Vault"))
        else:
            self.vault_path = Path(vault_path)

        # Ensure vault directory exists
        self.vault_path.mkdir(parents=True, exist_ok=True)

        # Define standard vault directories
        self.inbox_dir = self.vault_path / "Inbox"
        self.needs_action_dir = self.vault_path / "Needs_Action"
        self.plans_dir = self.vault_path / "Plans"
        self.in_progress_dir = self.vault_path / "In_Progress"
        self.done_dir = self.vault_path / "Done"
        self.pending_approval_dir = self.vault_path / "Pending_Approval"
        self.approved_dir = self.vault_path / "Approved"
        self.rejected_dir = self.vault_path / "Rejected"
        self.logs_dir = self.vault_path / "Logs"
        self.briefings_dir = self.vault_path / "Briefings"
        self.accounting_dir = self.vault_path / "Accounting"
        self.signals_dir = self.vault_path / "Signals"

        # Create directories if they don't exist
        self._create_vault_structure()

    def _create_vault_structure(self):
        """Create the standard vault directory structure with Platinum domain splits."""
        directories = [
            self.inbox_dir,
            self.needs_action_dir,
            self.plans_dir,
            self.in_progress_dir,
            self.done_dir,
            self.pending_approval_dir,
            self.approved_dir,
            self.rejected_dir,
            self.logs_dir,
            self.briefings_dir,
            self.accounting_dir,
            self.signals_dir
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            # Create domain subdirectories for critical folders
            if directory.name in ["Needs_Action", "Plans", "Pending_Approval"]:
                (directory / "Personal").mkdir(parents=True, exist_ok=True)
                (directory / "Business").mkdir(parents=True, exist_ok=True)

    def list_files_in_directory(self, directory: Path) -> List[Path]:
        """
        List all files in a specified directory.

        Args:
            directory: The directory to list files from

        Returns:
            List of file paths
        """
        if not directory.exists():
            return []

        files = []
        for item in directory.iterdir():
            if item.is_file():
                files.append(item)
        return files

    def get_inbox_files(self) -> List[Path]:
        """Get all files in the Inbox directory."""
        return self.list_files_in_directory(self.inbox_dir)

    def get_needs_action_files(self) -> List[Path]:
        """Get all files in the Needs_Action directory."""
        return self.list_files_in_directory(self.needs_action_dir)

    def get_done_files(self) -> List[Path]:
        """Get all files in the Done directory."""
        return self.list_files_in_directory(self.done_dir)

    def get_pending_approval_files(self) -> List[Path]:
        """Get all files in the Pending_Approval directory."""
        return self.list_files_in_directory(self.pending_approval_dir)

    def get_approved_files(self) -> List[Path]:
        """Get all files in the Approved directory."""
        return self.list_files_in_directory(self.approved_dir)

    def get_rejected_files(self) -> List[Path]:
        """Get all files in the Rejected directory."""
        return self.list_files_in_directory(self.rejected_dir)

    def claim_task(self, file_path: Path, agent_name: str) -> Optional[Path]:
        """
        Claim a task by moving it to In_Progress/<agent_name>/.
        Implements the 'Claim-by-Move' rule for Platinum tier.
        
        Args:
            file_path: Path to the task file
            agent_name: Name of the agent claiming the task
            
        Returns:
            New path of the file if successful, None otherwise
        """
        agent_dir = self.in_progress_dir / agent_name
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        destination = agent_dir / file_path.name
        if self.move_file(file_path, destination):
            return destination
        return None

    def vault_sync(self) -> bool:
        """
        Perform a Git-based vault sync.
        STRICT Security Rule: Credentials are excluded via .gitignore.
        
        Returns:
            True if sync was successful, False otherwise.
        """
        if is_dry_run():
            log_action("Would perform Git-based vault sync", actor="system", result="info", dry_run=True)
            return True

        import subprocess
        try:
            # Sync strategy: Add changes, commit, pull rebase, push
            subprocess.run(["git", "add", str(self.vault_path)], check=True)
            
            # Check if there are changes to commit
            status = subprocess.run(["git", "status", "--porcelain", str(self.vault_path)], 
                                   capture_output=True, text=True)
            if not status.stdout.strip():
                log_action("Vault sync: No changes to sync", actor="system", result="success")
                return True

            subprocess.run(["git", "commit", "-m", f"Vault sync: {datetime.now().isoformat()}"], check=True)
            subprocess.run(["git", "pull", "--rebase"], check=True)
            subprocess.run(["git", "push"], check=True)
            
            log_action("Vault sync completed successfully", actor="system", result="success")
            return True
        except subprocess.CalledProcessError as e:
            log_action("Vault sync failed", actor="system", result="error", details={"error": str(e)})
            return False

    def move_file(self, source: Path, destination: Path) -> bool:
        """
        Move a file from source to destination.

        Args:
            source: Source file path
            destination: Destination file path

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure destination directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)

            # Log the action
            action_details = {
                "source": str(source),
                "destination": str(destination)
            }

            if is_dry_run():
                log_action(
                    f"Would move file from {source} to {destination}",
                    actor="system",
                    details=action_details,
                    dry_run=True
                )
                return True
            else:
                # Actually move the file
                source.rename(destination)
                log_action(
                    f"Moved file from {source} to {destination}",
                    actor="system",
                    result="success",
                    details=action_details,
                    dry_run=False
                )
                return True
        except Exception as e:
            log_action(
                f"Failed to move file from {source} to {destination}",
                actor="system",
                result="error",
                details={"error": str(e), "source": str(source), "destination": str(destination)},
                dry_run=False
            )
            return False

    def move_to_needs_action(self, file_path: Path) -> bool:
        """Move a file to the Needs_Action directory."""
        destination = self.needs_action_dir / file_path.name
        return self.move_file(file_path, destination)

    def move_to_done(self, file_path: Path) -> bool:
        """Move a file to the Done directory."""
        destination = self.done_dir / file_path.name
        return self.move_file(file_path, destination)

    def move_to_pending_approval(self, file_path: Path) -> bool:
        """Move a file to the Pending_Approval directory."""
        destination = self.pending_approval_dir / file_path.name
        return self.move_file(file_path, destination)

    def move_to_approved(self, file_path: Path) -> bool:
        """Move a file to the Approved directory."""
        destination = self.approved_dir / file_path.name
        return self.move_file(file_path, destination)

    def move_to_rejected(self, file_path: Path) -> bool:
        """Move a file to the Rejected directory."""
        destination = self.rejected_dir / file_path.name
        return self.move_file(file_path, destination)

    def read_file(self, file_path: Path) -> Optional[str]:
        """
        Read the content of a file.

        Args:
            file_path: Path to the file to read

        Returns:
            File content as string, or None if error
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                log_action(
                    f"Read file {file_path}",
                    actor="system",
                    result="success",
                    details={"file_size": len(content)},
                    dry_run=False
                )
                return content
        except Exception as e:
            log_action(
                f"Failed to read file {file_path}",
                actor="system",
                result="error",
                details={"error": str(e)},
                dry_run=False
            )
            return None

    def write_file(self, file_path: Path, content: str) -> bool:
        """
        Write content to a file.

        Args:
            file_path: Path to the file to write
            content: Content to write to the file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure the parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            log_action(
                f"Wrote file {file_path}",
                actor="system",
                result="success",
                details={"file_size": len(content)},
                dry_run=False
            )
            return True
        except Exception as e:
            log_action(
                f"Failed to write file {file_path}",
                actor="system",
                result="error",
                details={"error": str(e)},
                dry_run=False
            )
            return False

    def get_vault_stats(self) -> Dict[str, Any]:
        """Get statistics about the vault."""
        stats = {}
        directories = {
            "inbox": self.inbox_dir,
            "needs_action": self.needs_action_dir,
            "plans": self.plans_dir,
            "done": self.done_dir,
            "pending_approval": self.pending_approval_dir,
            "approved": self.approved_dir,
            "rejected": self.rejected_dir,
            "logs": self.logs_dir,
            "briefings": self.briefings_dir,
            "accounting": self.accounting_dir
        }

        for name, directory in directories.items():
            try:
                file_count = len([f for f in directory.iterdir() if f.is_file()])
                stats[name] = file_count
            except:
                stats[name] = 0  # Directory might not exist yet

        stats["total_files"] = sum(stats.values())
        stats["vault_path"] = str(self.vault_path)

        return stats

    def create_initial_dashboard(self):
        """Create or update the dashboard with current stats."""
        stats = self.get_vault_stats()
        dashboard_path = self.vault_path / "Dashboard.md"

        content = f"""# AI Employee Dashboard

**Status**: Active
**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## System Overview
- **Active Watchers**: 0
- **Pending Actions**: {stats.get('needs_action', 0)}
- **Completed Today**: {stats.get('done', 0)}
- **System Uptime**: Initializing

## Task Queue
### Needs Action
"""

        # Add files in needs_action to the dashboard
        needs_action_files = self.get_needs_action_files()
        if needs_action_files:
            for file_path in needs_action_files:
                content += f"- {file_path.name}\n"
        else:
            content += "- No tasks pending\n"

        content += """
### In Progress
"""

        # Add files in In_Progress to the dashboard
        for agent_dir in self.in_progress_dir.iterdir():
            if agent_dir.is_dir():
                content += f"#### Agent: {agent_dir.name}\n"
                agent_files = self.list_files_in_directory(agent_dir)
                if agent_files:
                    for file_path in agent_files:
                        content += f"- {file_path.name}\n"
                else:
                    content += "- No tasks in progress\n"

        content += """
### Completed Today
"""

        # Add files in done to the dashboard
        done_files = self.get_done_files()
        if done_files:
            for file_path in done_files:
                content += f"- {file_path.name}\n"
        else:
            content += "- No tasks completed today\n"

        content += """
## Alerts
- No alerts

## System Health
- All systems nominal

---
*Generated by Personal AI Employee System*
*Last Updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "*"

        self.write_file(dashboard_path, content)


# Global vault manager instance
vault_manager = VaultManager()


def get_vault_manager() -> VaultManager:
    """Get the global vault manager instance."""
    return vault_manager