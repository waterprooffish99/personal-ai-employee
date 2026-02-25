import json
import structlog
from datetime import datetime
from pathlib import Path
import os
from typing import Any, Dict, Optional

from .env_manager import get_env
from .dry_run import log_action


class JSONLogger:
    """JSON-compliant logging system for the AI Employee system."""

    def __init__(self, log_dir: str = None):
        """
        Initialize the JSON logger.

        Args:
            log_dir: Directory to store log files (defaults to VAULT_PATH/Logs)
        """
        if log_dir is None:
            vault_path = get_env("VAULT_PATH", "AI_Employee_Vault")
            self.log_dir = Path(vault_path) / "Logs"
        else:
            self.log_dir = Path(log_dir)

        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Configure structlog
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        self.logger = structlog.get_logger()

    def _write_log_to_file(self, log_entry: Dict[str, Any]):
        """Write log entry to a dated JSON file."""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file_path = self.log_dir / f"{today}.json"

        # Add the entry to the log file
        if log_file_path.exists():
            with open(log_file_path, 'r', encoding='utf-8') as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []

        logs.append(log_entry)

        with open(log_file_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

    def log(self, level: str, action: str, actor: str, result: str = None,
            details: Dict[str, Any] = None, dry_run: bool = False):
        """
        Log an action with JSON-compliant format.

        Args:
            level: Log level (info, warning, error, critical)
            action: Description of the action being logged
            actor: Who or what performed the action (AI, human, system)
            result: Result of the action
            details: Additional details about the action
            dry_run: Whether this action was in dry run mode
        """
        timestamp = datetime.now().isoformat()

        log_entry = {
            "timestamp": timestamp,
            "level": level.lower(),
            "action": action,
            "actor": actor,
            "result": result or "unknown",
            "details": details or {},
            "dry_run": dry_run
        }

        # Log to file
        self._write_log_to_file(log_entry)

        # Also log to console using structlog
        getattr(self.logger, level.lower())(
            action=action,
            actor=actor,
            result=result,
            details=details,
            dry_run=dry_run
        )

    def info(self, action: str, actor: str = "system", result: str = None,
             details: Dict[str, Any] = None, dry_run: bool = False):
        """Log an info level message."""
        self.log("info", action, actor, result, details, dry_run)

    def warning(self, action: str, actor: str = "system", result: str = None,
                details: Dict[str, Any] = None, dry_run: bool = False):
        """Log a warning level message."""
        self.log("warning", action, actor, result, details, dry_run)

    def error(self, action: str, actor: str = "system", result: str = None,
              details: Dict[str, Any] = None, dry_run: bool = False):
        """Log an error level message."""
        self.log("error", action, actor, result, details, dry_run)

    def critical(self, action: str, actor: str = "system", result: str = None,
                 details: Dict[str, Any] = None, dry_run: bool = False):
        """Log a critical level message."""
        self.log("critical", action, actor, result, details, dry_run)

    def log_action(self, action: str, actor: str = "AI", result: str = None,
                   details: Dict[str, Any] = None, dry_run: bool = None):
        """
        Log an action taken by the AI employee system.

        Args:
            action: Description of the action
            actor: Who performed the action (default "AI")
            result: Result of the action
            details: Additional details
            dry_run: Whether this was a dry run (defaults to current dry_run status)
        """
        if dry_run is None:
            from .dry_run import is_dry_run
            dry_run = is_dry_run()

        self.info(action, actor, result, details, dry_run)


# Global logger instance
json_logger = JSONLogger()


def get_logger() -> JSONLogger:
    """Get the global JSON logger instance."""
    return json_logger


def log_action(action: str, actor: str = "AI", result: str = None,
               details: Dict[str, Any] = None, dry_run: bool = None):
    """Log an action using the global logger."""
    if dry_run is None:
        from .dry_run import is_dry_run
        dry_run = is_dry_run()

    json_logger.log_action(action, actor, result, details, dry_run)