import time
from pathlib import Path
from typing import Optional, Dict, Any
import watchdog.events
from watchdog.observers import Observer

from .base_watcher import BaseWatcher
from ..vault.vault_manager import vault_manager, get_vault_manager
from ..utils.logger import log_action
from ..utils.dry_run import is_dry_run


class FilesystemWatcher(BaseWatcher):
    """
    FilesystemWatcher monitors the /Inbox directory for new files and creates
    action files in the vault when new files are detected.
    """

    def __init__(self, watch_path: str = None, poll_interval: int = 5):
        """
        Initialize the FilesystemWatcher.

        Args:
            watch_path: Path to watch (defaults to vault's Inbox directory)
            poll_interval: Interval in seconds between filesystem checks
        """
        super().__init__("FilesystemWatcher", poll_interval)

        if watch_path is None:
            vault_path = vault_manager.vault_path
            self.watch_path = vault_path / "Inbox"
        else:
            self.watch_path = Path(watch_path)

        # Create the watched directory if it doesn't exist
        self.watch_path.mkdir(parents=True, exist_ok=True)

        self.observer: Optional[Observer] = None
        self._last_processed_files = set()

        # Get initial list of files to avoid processing existing ones on startup
        self._initialize_existing_files()

    def _initialize_existing_files(self):
        """Initialize the set of files that already exist to avoid processing them."""
        if self.watch_path.exists():
            for file_path in self.watch_path.iterdir():
                if file_path.is_file():
                    self._last_processed_files.add(file_path.name)

    def check_for_updates(self) -> bool:
        """
        Check for new files in the watched directory.

        Returns:
            True if new files were detected, False otherwise
        """
        if not self.watch_path.exists():
            log_action(
                f"Watch path does not exist: {self.watch_path}",
                actor="system",
                result="error",
                dry_run=is_dry_run()
            )
            return False

        new_files_detected = False
        current_files = set()

        # Get current files in the watched directory
        for file_path in self.watch_path.iterdir():
            if file_path.is_file():
                current_files.add(file_path.name)

        # Find new files that weren't there before
        new_files = current_files - self._last_processed_files

        for filename in new_files:
            file_path = self.watch_path / filename

            try:
                # Process the new file
                self._process_incoming_file(file_path)
                new_files_detected = True
                log_action(
                    f"Processed new file: {filename}",
                    actor="system",
                    result="success",
                    details={"file_path": str(file_path)},
                    dry_run=is_dry_run()
                )
            except Exception as e:
                log_action(
                    f"Failed to process file: {filename}",
                    actor="system",
                    result="error",
                    details={"error": str(e), "file_path": str(file_path)},
                    dry_run=is_dry_run()
                )

        # Update the set of processed files
        self._last_processed_files = current_files

        return new_files_detected

    def _process_incoming_file(self, file_path: Path):
        """
        Process an incoming file by creating an action file in the vault.

        Args:
            file_path: Path to the incoming file
        """
        # Read the content of the incoming file
        content = vault_manager.read_file(file_path)
        if content is None:
            log_action(
                f"Could not read file content: {file_path}",
                actor="system",
                result="error",
                dry_run=is_dry_run()
            )
            return

        # Create an action file based on the incoming file
        self._create_action_file(file_path, content)

    def _create_action_file(self, source_file: Path, content: str):
        """
        Create an action file in the Needs_Action directory based on the incoming file.

        Args:
            source_file: The original incoming file
            content: Content of the incoming file
        """
        # Create a meaningful name for the action file
        action_filename = f"action_{source_file.stem}_{int(time.time())}.md"
        action_path = vault_manager.needs_action_dir / action_filename

        # Create the action file with instructions for Claude
        action_content = f"""# Action Request from File Monitor

**Source File**: {source_file.name}
**Received**: {time.strftime('%Y-%m-%d %H:%M:%S')}
**Action Required**:

{content}

---

Please process this request and take appropriate action.
If you need more information, please indicate what is needed.
When completed, move this file to the Done directory.
"""

        # Write the action file
        success = vault_manager.write_file(action_path, action_content)

        if success:
            log_action(
                f"Created action file: {action_filename}",
                actor="system",
                result="success",
                details={"source_file": str(source_file), "action_file": str(action_path)},
                dry_run=is_dry_run()
            )
        else:
            log_action(
                f"Failed to create action file: {action_filename}",
                actor="system",
                result="error",
                details={"source_file": str(source_file)},
                dry_run=is_dry_run()
            )

    def start(self):
        """Start the watcher using the base class functionality."""
        log_action(
            f"FilesystemWatcher starting, watching: {self.watch_path}",
            actor="system",
            result="success",
            dry_run=is_dry_run()
        )
        super().start()

    def start_daemon(self):
        """Start the watcher in daemon mode."""
        log_action(
            f"FilesystemWatcher starting in daemon mode, watching: {self.watch_path}",
            actor="system",
            result="success",
            dry_run=is_dry_run()
        )
        super().start_daemon()

    def stop(self):
        """Stop the watcher."""
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()

        log_action(
            f"FilesystemWatcher stopped, was watching: {self.watch_path}",
            actor="system",
            result="success",
            dry_run=is_dry_run()
        )
        super().stop()