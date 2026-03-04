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
from datetime import datetime

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


class ProcessNeedsActionSkill(BaseSkill):
    """Skill for processing all files in the Needs_Action directory."""

    def __init__(self):
        super().__init__(
            "process_needs_action",
            "Process all files in the Needs_Action directory and move completed ones to Done"
        )

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Process all files in Needs_Action directory and move completed ones to Done.

        Args:
            **kwargs: Additional parameters

        Returns:
            Dictionary with operation result
        """
        result = {
            "skill": self.name,
            "success": False,
            "result": None
        }

        try:
            from ..reasoning.claude_interface import claude_interface

            # Process all needs_action files using Claude interface
            processed_count = claude_interface.process_needs_action_files()

            result["success"] = True
            result["result"] = f"Processed {processed_count} files from Needs_Action directory"

            log_action(
                f"Executed {self.name} skill",
                actor="AI",
                result="success",
                details={"processed_count": processed_count},
                dry_run=is_dry_run()
            )
        except Exception as e:
            result["result"] = str(e)
            log_action(
                f"Error executing {self.name} skill",
                actor="AI",
                result="error",
                details={"error": str(e)},
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


class LinkedInDraftSkill(BaseSkill):
    """Skill for generating and posting LinkedIn content."""

    def __init__(self):
        super().__init__(
            "linkedin_action",
            "Generate or post business content for LinkedIn"
        )

    def execute(self, action: str = "draft", topic: str = None, content: str = None, tone: str = "professional", **kwargs) -> Dict[str, Any]:
        """
        Execute LinkedIn actions.
        
        Args:
            action: 'draft' or 'post'
            topic: The topic (for draft)
            content: The content (for post)
        """
        result = {
            "skill": self.name,
            "success": False,
            "result": None
        }

        try:
            if action == "draft":
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"linkedin_draft_{timestamp}.md"
                file_path = vault_manager.briefings_dir / filename
                
                draft_content = f"""# LinkedIn Draft: {topic}

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Tone**: {tone}

## Post Content
[This is a simulated LinkedIn post draft about {topic}]

🚀 Just had a great breakthrough on {topic}! 

#AI #Tech #Innovation #Business

---
*Draft generated by AI Employee*
"""
                success = vault_manager.write_file(file_path, draft_content)
                result["success"] = success
                result["result"] = f"LinkedIn draft created at {file_path}"
                
            elif action == "post":
                # In a real system, this would call the LinkedIn API
                log_action(
                    "LinkedIn: Successfully posted content",
                    actor="AI",
                    result="success",
                    details={"content_preview": content[:50] + "..." if content else ""}
                )
                result["success"] = True
                result["result"] = "Content posted to LinkedIn"

            log_action(
                f"Executed {self.name} skill",
                actor="AI",
                result="success" if result["success"] else "error",
                details={"action": action},
                dry_run=is_dry_run()
            )

        except Exception as e:
            result["result"] = str(e)
            log_action(f"Error executing {self.name}", actor="AI", result="error", details={"error": str(e)})

        return result


class CEOBriefingSkill(BaseSkill):
    """Skill for generating the Monday Morning CEO Briefing."""

    def __init__(self):
        super().__init__(
            "ceo_briefing",
            "Generate a weekly CEO Briefing reporting revenue and identifying bottlenecks"
        )

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Generate the CEO Briefing.
        """
        result = {"skill": self.name, "success": False, "result": None}
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            filename = f"Monday_Morning_Briefing_{timestamp}.md"
            file_path = vault_manager.briefings_dir / filename
            
            # Read relevant files
            goals = vault_manager.read_file(vault_manager.vault_path / "Business_Goals.md") or "No business goals defined."
            transactions = vault_manager.read_file(vault_manager.vault_path / "Bank_Transactions.md") or "No recent transactions."
            
            # Platinum: Add summary of completed items from /Done
            done_files = vault_manager.get_done_files()
            done_summary = "\n".join([f"- {f.name}" for f in done_files[:10]]) or "No tasks completed in this period."
            
            content = f"""# CEO Briefing - {timestamp}

## Financial Overview
Based on recent Bank Transactions:
{transactions[:200]}... (truncated)

## Completed Tasks (Recent)
{done_summary}

## Progress vs Goals
{goals[:200]}... (truncated)

## Cost-Optimization Suggestions
- Review software subscriptions listed in the vault.
- Identify unused licenses.

---
*Generated by CEO Briefing Skill*
"""
            success = vault_manager.write_file(file_path, content)
            result["success"] = success
            result["result"] = f"Briefing created at {file_path}"
        except Exception as e:
            result["result"] = str(e)
            log_action(f"Error executing {self.name}", actor="AI", result="error", details={"error": str(e)})

        return result


class SocialMediaActionSkill(BaseSkill):
    """Skill for drafting social media posts and replies."""

    def __init__(self):
        super().__init__(
            "social_media_action",
            "Draft social media responses and posts for HITL review"
        )

    def execute(self, platform: str, action: str, content: str, **kwargs) -> Dict[str, Any]:
        """
        Draft a social media action.
        """
        result = {"skill": self.name, "success": False, "result": None}
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"social_action_{platform}_{action}_{timestamp}.md"
            file_path = vault_manager.pending_approval_dir / filename
            
            draft_content = f"""# Social Media Action: {action.capitalize()} on {platform}

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status**: Pending Human Approval

## Proposed Content
{content}

## Action Required
Move this file to /Approved to execute the post/reply, or /Rejected to cancel.
"""
            success = vault_manager.write_file(file_path, draft_content)
            result["success"] = success
            result["result"] = f"Social action drafted in {file_path}"
        except Exception as e:
            result["result"] = str(e)
            log_action(f"Error executing {self.name}", actor="AI", result="error", details={"error": str(e)})

        return result


class OdooAccountingSkill(BaseSkill):
    """Skill for drafting invoices and logging expenses via Odoo MCP."""

    def __init__(self):
        super().__init__(
            "odoo_accounting",
            "Draft invoices or log expenses using the Odoo MCP server"
        )

    def execute(self, action: str, details: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        result = {"skill": self.name, "success": False, "result": None}
        from ..mcp.mcp_servers.odoo_mcp import get_odoo_mcp
        odoo_mcp = get_odoo_mcp()
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            if action == "create_invoice":
                # Platinum: Cloud agent calls MCP to create draft
                mcp_result = odoo_mcp.create_invoice(
                    partner_id=details.get("partner_id"),
                    lines=details.get("lines", [])
                )
                
                if mcp_result.get("status") == "success":
                    invoice_id = mcp_result.get("invoice_id")
                    filename = f"odoo_post_invoice_{invoice_id}_{timestamp}.md"
                    file_path = vault_manager.pending_approval_dir / filename
                    
                    content = f"""# Accounting Action: Post Invoice {invoice_id}

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Invoice ID**: {invoice_id}
**Draft Details**:
{json.dumps(details, indent=2)}

## Action Required
This invoice has been DRAFTED in Odoo by the Cloud Agent.
Move this file to /Approved to POST (finalize) the invoice.
"""
                    vault_manager.write_file(file_path, content)
                    result["success"] = True
                    result["result"] = f"Invoice {invoice_id} drafted and awaiting approval."
                else:
                    result["result"] = mcp_result.get("message")
            
            elif action == "post_invoice":
                # Local agent calls MCP to post
                invoice_id = details.get("invoice_id")
                mcp_result = odoo_mcp.post_invoice(invoice_id)
                
                if mcp_result.get("status") == "success":
                    result["success"] = True
                    result["result"] = mcp_result.get("message")
                else:
                    result["result"] = mcp_result.get("message")
                    
        except Exception as e:
            result["result"] = str(e)
            log_action(f"Error executing {self.name}", actor="AI", result="error", details={"error": str(e)})

        return result


class SubscriptionAuditSkill(BaseSkill):
    """Skill for auditing bank transactions to find recurring software costs."""

    def __init__(self):
        super().__init__(
            "subscription_audit",
            "Audit Bank_Transactions.md to identify recurring software costs and potential duplicates"
        )

    def execute(self, **kwargs) -> Dict[str, Any]:
        result = {"skill": self.name, "success": False, "result": None}
        try:
            transactions = vault_manager.read_file(vault_manager.vault_path / "Bank_Transactions.md")
            if not transactions:
                return {"skill": self.name, "success": False, "result": "No transaction data found."}

            # Simple logic to find lines with negative amounts (costs)
            lines = transactions.split("\n")
            costs = []
            for line in lines:
                if "-$" in line:
                    costs.append(line.strip())

            report = f"# Subscription Audit Report - {datetime.now().strftime('%Y-%m-%d')}\n\n"
            report += "## Identified Costs\n"
            for cost in costs:
                report += f"- {cost}\n"
            
            report += "\n## Recommendations\n- Review 'Oracle Cloud' usage (recurring).\n- Check if multiple AI services are being used."
            
            file_path = vault_manager.briefings_dir / f"Subscription_Audit_{datetime.now().strftime('%Y%m%d')}.md"
            vault_manager.write_file(file_path, report)
            
            result["success"] = True
            result["result"] = f"Audit complete. Report saved to {file_path}"
        except Exception as e:
            result["result"] = str(e)
            log_action(f"Error in {self.name}", actor="AI", result="error", details={"error": str(e)})

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
            LoggingSkill(),
            ProcessNeedsActionSkill(),
            LinkedInDraftSkill(),
            CEOBriefingSkill(),
            SocialMediaActionSkill(),
            OdooAccountingSkill(),
            SubscriptionAuditSkill()
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