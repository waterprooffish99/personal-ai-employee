from .env_manager import get_env_bool


class DryRunManager:
    """Manages the global DRY_RUN flag for the AI Employee system."""

    def __init__(self):
        """Initialize the DryRunManager with the environment setting."""
        self._dry_run = get_env_bool("DRY_RUN", default=True)

    @property
    def enabled(self) -> bool:
        """Check if dry run mode is enabled."""
        return self._dry_run

    @enabled.setter
    def enabled(self, value: bool):
        """Set the dry run mode."""
        self._dry_run = value

    def execute_if_real(self, func, *args, **kwargs):
        """
        Execute a function only if not in dry run mode.

        Args:
            func: The function to execute
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            The result of the function if not in dry run mode,
            otherwise a dry run message
        """
        if self.enabled:
            print(f"[DRY RUN] Would execute: {func.__name__} with args: {args}, kwargs: {kwargs}")
            return f"[DRY RUN] Executed {func.__name__}"
        else:
            return func(*args, **kwargs)

    def log_action(self, action_description: str):
        """
        Log an action that would be performed.

        Args:
            action_description: Description of the action that would be performed
        """
        if self.enabled:
            print(f"[DRY RUN] Would perform action: {action_description}")
        else:
            print(f"[REAL] Performing action: {action_description}")


# Global dry run manager instance
dry_run_manager = DryRunManager()


def is_dry_run() -> bool:
    """Check if dry run mode is enabled globally."""
    return dry_run_manager.enabled


def execute_if_real(func, *args, **kwargs):
    """Execute a function only if not in dry run mode."""
    return dry_run_manager.execute_if_real(func, *args, **kwargs)


def log_action(action_description: str):
    """Log an action that would be performed."""
    dry_run_manager.log_action(action_description)