"""
Agent Skills Framework for the AI Employee System.

This module provides a framework for creating reusable agent skills
that can be called by Claude to perform specific actions.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from pathlib import Path
import json
import time

from ..vault.vault_manager import vault_manager
from ..utils.logger import log_action
from ..utils.dry_run import is_dry_run, execute_if_real


class BaseSkill(ABC):
    """Abstract base class for all agent skills."""

    def __init__(self, name: str, description: str):
        """
        Initialize the skill.

        Args:
            name: Name of the skill
            description: Description of what the skill does
        """
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the skill with given parameters.

        Args:
            **kwargs: Skill-specific parameters

        Returns:
            Dictionary containing the result of the execution
        """
        pass


class FileOperationSkill(BaseSkill):
    """Skill for performing file operations in the vault."""

    def __init__(self):
        super().__init__(
            "file_operation",
            "Perform file operations in the vault directories"
        )

    def execute(self, operation: str, file_path: str = None, content: str = None, **kwargs) -> Dict[str, Any]:
        """
        Execute file operations.

        Args:
            operation: Type of operation ('read', 'write', 'move', 'list')
            file_path: Path to the file to operate on
            content: Content to write (for write operations)
            **kwargs: Additional parameters

        Returns:
            Dictionary with operation result
        """
        result = {
            "skill": self.name,
            "operation": operation,
            "success": False,
            "result": None
        }

        try:
            file_path_obj = Path(file_path) if file_path else None

            if operation == "read":
                content = vault_manager.read_file(file_path_obj)
                result["result"] = content
                result["success"] = content is not None
            elif operation == "write":
                if content:
                    success = vault_manager.write_file(file_path_obj, content)
                    result["success"] = success
                    result["result"] = f"File {file_path} written successfully" if success else "Failed to write file"
            elif operation == "move":
                source_path = Path(kwargs.get("source_path", ""))
                dest_dir_name = kwargs.get("destination", "Done")

                # Map destination names to actual directories
                dest_dirs = {
                    "inbox": vault_manager.inbox_dir,
                    "needs_action": vault_manager.needs_action_dir,
                    "plans": vault_manager.plans_dir,
                    "done": vault_manager.done_dir,
                    "pending_approval": vault_manager.pending_approval_dir,
                    "approved": vault_manager.approved_dir,
                    "rejected": vault_manager.rejected_dir
                }

                if dest_dir_name.lower() in dest_dirs:
                    dest_path = dest_dirs[dest_dir_name.lower()] / source_path.name
                    success = vault_manager.move_file(source_path, dest_path)
                    result["success"] = success
                    result["result"] = f"File moved to {dest_path}" if success else "Failed to move file"
                else:
                    result["result"] = f"Unknown destination: {dest_dir_name}"
            elif operation == "list":
                directory_name = kwargs.get("directory", "needs_action")

                # Get files from the specified directory
                dir_mapping = {
                    "inbox": vault_manager.get_inbox_files,
                    "needs_action": vault_manager.get_needs_action_files,
                    "done": vault_manager.get_done_files,
                    "pending_approval": vault_manager.get_pending_approval_files,
                    "approved": vault_manager.get_approved_files,
                    "rejected": vault_manager.get_rejected_files,
                    "plans": lambda: list((vault_manager.vault_path / "Plans").iterdir()) if (vault_manager.vault_path / "Plans").exists() else []
                }

                if directory_name.lower() in dir_mapping:
                    files = dir_mapping[directory_name.lower()]()
                    result["result"] = [str(f) for f in files]
                    result["success"] = True
                else:
                    result["result"] = f"Unknown directory: {directory_name}"
            else:
                result["result"] = f"Unknown operation: {operation}"

            log_action(
                f"Executed {self.name} skill",
                actor="AI",
                result="success" if result["success"] else "error",
                details={"operation": operation, "file_path": file_path},
                dry_run=is_dry_run()
            )
        except Exception as e:
            result["result"] = str(e)
            log_action(
                f"Error executing {self.name} skill",
                actor="AI",
                result="error",
                details={"error": str(e), "operation": operation, "file_path": file_path},
                dry_run=is_dry_run()
            )

        return result


class DashboardUpdateSkill(BaseSkill):
    """Skill for updating the dashboard."""

    def __init__(self):
        super().__init__(
            "dashboard_update",
            "Update the dashboard with current system status"
        )

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Update the dashboard.

        Args:
            **kwargs: Additional parameters

        Returns:
            Dictionary with operation result
        """
        try:
            vault_manager.create_initial_dashboard()

            result = {
                "skill": self.name,
                "success": True,
                "result": "Dashboard updated successfully"
            }

            log_action(
                "Dashboard updated via skill",
                actor="AI",
                result="success",
                dry_run=is_dry_run()
            )
        except Exception as e:
            result = {
                "skill": self.name,
                "success": False,
                "result": str(e)
            }

            log_action(
                "Error updating dashboard via skill",
                actor="AI",
                result="error",
                details={"error": str(e)},
                dry_run=is_dry_run()
            )

        return result


class LoggingSkill(BaseSkill):
    """Skill for logging system events."""

    def __init__(self):
        super().__init__(
            "logging",
            "Log events to the system log"
        )

    def execute(self, message: str, level: str = "info", **kwargs) -> Dict[str, Any]:
        """
        Log a message.

        Args:
            message: The message to log
            level: Log level ('info', 'warning', 'error', 'critical')
            **kwargs: Additional parameters

        Returns:
            Dictionary with operation result
        """
        try:
            # Call the appropriate logging function based on level
            from ..utils.logger import json_logger
            getattr(json_logger, level.lower())(
                message,
                actor=kwargs.get("actor", "AI"),
                result=kwargs.get("result", "success"),
                details=kwargs
            )

            result = {
                "skill": self.name,
                "success": True,
                "result": f"Logged message at {level} level: {message}"
            }
        except Exception as e:
            result = {
                "skill": self.name,
                "success": False,
                "result": str(e)
            }

        return result


# Global registry of available skills
class SkillRegistry:
    """Registry to manage available skills."""

    def __init__(self):
        self.skills: Dict[str, BaseSkill] = {}
        self._register_default_skills()

    def _register_default_skills(self):
        """Register default skills."""
        default_skills = [
            FileOperationSkill(),
            DashboardUpdateSkill(),
            LoggingSkill()
        ]

        for skill in default_skills:
            self.register_skill(skill)

    def register_skill(self, skill: BaseSkill):
        """Register a skill."""
        self.skills[skill.name.lower()] = skill

    def get_skill(self, name: str) -> Optional[BaseSkill]:
        """Get a skill by name."""
        return self.skills.get(name.lower())

    def execute_skill(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute a skill by name."""
        skill = self.get_skill(name)
        if skill:
            return skill.execute(**kwargs)
        else:
            return {
                "skill": name,
                "success": False,
                "result": f"Skill '{name}' not found"
            }

    def list_skills(self) -> List[str]:
        """List all available skills."""
        return list(self.skills.keys())


# Global skill registry instance
skill_registry = SkillRegistry()


def get_skill_registry() -> SkillRegistry:
    """Get the global skill registry instance."""
    return skill_registry


def execute_skill(name: str, **kwargs) -> Dict[str, Any]:
    """Execute a skill by name using the global registry."""
    return skill_registry.execute_skill(name, **kwargs)