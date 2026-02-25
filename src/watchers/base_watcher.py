from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import threading
import time
from pathlib import Path

from ..utils.logger import log_action
from ..utils.dry_run import is_dry_run


class BaseWatcher(ABC):
    """Abstract base class for all watchers in the AI Employee system."""

    def __init__(self, name: str, poll_interval: int = 30):
        """
        Initialize the watcher.

        Args:
            name: Name of the watcher
            poll_interval: Interval in seconds between checks (default 30)
        """
        self.name = name
        self.poll_interval = poll_interval
        self.running = False
        self.thread: Optional[threading.Thread] = None

    @abstractmethod
    def check_for_updates(self) -> bool:
        """
        Check for updates/events. This method must be implemented by subclasses.

        Returns:
            True if new events were detected, False otherwise
        """
        pass

    def start(self):
        """Start the watcher in the main thread."""
        if self.running:
            print(f"Watcher {self.name} is already running")
            return

        self.running = True
        log_action(
            f"Starting watcher: {self.name}",
            actor="system",
            result="success",
            dry_run=is_dry_run()
        )

        try:
            while self.running:
                try:
                    self.check_for_updates()
                except Exception as e:
                    log_action(
                        f"Error in watcher {self.name}",
                        actor="system",
                        result="error",
                        details={"error": str(e)},
                        dry_run=is_dry_run()
                    )
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            self.stop()

    def start_daemon(self):
        """Start the watcher in a separate daemon thread."""
        if self.running:
            print(f"Watcher {self.name} is already running")
            return

        self.running = True

        def run():
            log_action(
                f"Starting daemon watcher: {self.name}",
                actor="system",
                result="success",
                dry_run=is_dry_run()
            )

            try:
                while self.running:
                    try:
                        self.check_for_updates()
                    except Exception as e:
                        log_action(
                            f"Error in daemon watcher {self.name}",
                            actor="system",
                            result="error",
                            details={"error": str(e)},
                            dry_run=is_dry_run()
                        )
                    time.sleep(self.poll_interval)
            except Exception as e:
                if self.running:  # Only log error if not intentional shutdown
                    log_action(
                        f"Unexpected error in daemon watcher {self.name}",
                        actor="system",
                        result="error",
                        details={"error": str(e)},
                        dry_run=is_dry_run()
                    )

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the watcher."""
        if not self.running:
            print(f"Watcher {self.name} is not running")
            return

        print(f"Stopping watcher {self.name}...")
        self.running = False

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish

        log_action(
            f"Stopped watcher: {self.name}",
            actor="system",
            result="success",
            dry_run=is_dry_run()
        )

    def run_once(self):
        """Run a single check cycle."""
        if self.running:
            print(f"Watcher {self.name} is already running")
            return

        self.running = True
        try:
            self.check_for_updates()
        except Exception as e:
            log_action(
                f"Error in single run of watcher {self.name}",
                actor="system",
                result="error",
                details={"error": str(e)},
                dry_run=is_dry_run()
            )
        finally:
            self.running = False