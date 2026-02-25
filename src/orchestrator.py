#!/usr/bin/env python3
"""
Orchestrator for the Personal AI Employee System.

This script serves as the master process for logic glue, coordinating
the various components of the AI employee system.
"""

import os
import sys
import time
import signal
import threading
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

# Add the project root to the path so we can import modules correctly
# The orchestrator is in src/ so we need to go up one level to import as src.module
project_root = Path(__file__).parent.parent  # Go from src/ to project root
sys.path.insert(0, str(project_root))

from src.utils.env_manager import get_env, get_env_bool, get_env_int
from src.utils.dry_run import dry_run_manager, is_dry_run
from src.utils.logger import json_logger, log_action
from src.vault.vault_manager import vault_manager, get_vault_manager
from src.watchers.base_watcher import BaseWatcher
from src.watchers.filesystem_watcher import FilesystemWatcher
from src.reasoning.claude_interface import claude_interface


class Orchestrator:
    """Main orchestrator for the AI Employee system."""

    def __init__(self):
        """Initialize the orchestrator."""
        self.watchers: List[BaseWatcher] = []
        self.running = False
        self.daemon = False

        # Set up signal handling for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\nReceived signal {signum}, shutting down gracefully...")
        self.stop()
        sys.exit(0)

    def add_watcher(self, watcher: BaseWatcher):
        """Add a watcher to the orchestrator."""
        self.watchers.append(watcher)
        log_action(
            f"Added watcher: {watcher.__class__.__name__}",
            actor="system",
            details={"watcher_count": len(self.watchers)},
            dry_run=is_dry_run()
        )

    def start_watchers(self):
        """Start all registered watchers."""
        for watcher in self.watchers:
            try:
                if self.daemon:
                    watcher.start_daemon()
                else:
                    watcher.start()
                log_action(
                    f"Started watcher: {watcher.__class__.__name__}",
                    actor="system",
                    result="success",
                    dry_run=is_dry_run()
                )
            except Exception as e:
                log_action(
                    f"Failed to start watcher: {watcher.__class__.__name__}",
                    actor="system",
                    result="error",
                    details={"error": str(e)},
                    dry_run=is_dry_run()
                )

    def stop_watchers(self):
        """Stop all registered watchers."""
        for watcher in self.watchers:
            try:
                watcher.stop()
                log_action(
                    f"Stopped watcher: {watcher.__class__.__name__}",
                    actor="system",
                    result="success",
                    dry_run=is_dry_run()
                )
            except Exception as e:
                log_action(
                    f"Failed to stop watcher: {watcher.__class__.__name__}",
                    actor="system",
                    result="error",
                    details={"error": str(e)},
                    dry_run=is_dry_run()
                )

    def start(self):
        """Start the orchestrator and all watchers."""
        if self.running:
            print("Orchestrator already running")
            return

        self.running = True
        log_action(
            "Starting AI Employee orchestrator",
            actor="system",
            result="success",
            details={"watcher_count": len(self.watchers)},
            dry_run=is_dry_run()
        )

        # Update dashboard
        vault_manager.create_initial_dashboard()

        # Start all watchers
        self.start_watchers()

        print(f"Orchestrator started with {len(self.watchers)} watchers")
        print(f"DRY_RUN mode: {is_dry_run()}")
        print(f"Vault path: {vault_manager.vault_path}")

        # Keep the main thread alive if running in daemon mode
        if self.daemon:
            try:
                while self.running:
                    time.sleep(1)
                    # Process Claude tasks periodically
                    from src.reasoning.claude_interface import claude_interface
                    claude_interface.run_processing_cycle()

                    # Update dashboard periodically
                    if time.time() % 300 < 1:  # Update every 5 minutes
                        vault_manager.create_initial_dashboard()
            except KeyboardInterrupt:
                self.stop()

    def stop(self):
        """Stop the orchestrator and all watchers."""
        if not self.running:
            print("Orchestrator not running")
            return

        print("Stopping orchestrator...")
        self.running = False

        # Stop all watchers
        self.stop_watchers()

        log_action(
            "Stopped AI Employee orchestrator",
            actor="system",
            result="success",
            dry_run=is_dry_run()
        )
        print("Orchestrator stopped")

    def run_once(self):
        """Run a single cycle of all watchers (non-daemon mode)."""
        if self.running:
            print("Orchestrator already running")
            return

        self.running = True
        log_action(
            "Running single cycle of AI Employee orchestrator",
            actor="system",
            result="success",
            details={"watcher_count": len(self.watchers)},
            dry_run=is_dry_run()
        )

        # Update dashboard
        vault_manager.create_initial_dashboard()

        # Run all watchers once
        for watcher in self.watchers:
            try:
                watcher.run_once()
                log_action(
                    f"Ran watcher once: {watcher.__class__.__name__}",
                    actor="system",
                    result="success",
                    dry_run=is_dry_run()
                )
            except Exception as e:
                log_action(
                    f"Failed to run watcher once: {watcher.__class__.__name__}",
                    actor="system",
                    result="error",
                    details={"error": str(e)},
                    dry_run=is_dry_run()
                )

        # Process Claude tasks after running watchers
        from src.reasoning.claude_interface import claude_interface
        claude_interface.run_processing_cycle()

        # Update dashboard after running
        vault_manager.create_initial_dashboard()

        self.running = False
        print(f"Completed single cycle with {len(self.watchers)} watchers")


def main():
    """Main entry point for the orchestrator."""
    import argparse

    parser = argparse.ArgumentParser(description='AI Employee Orchestrator')
    parser.add_argument('--daemon', action='store_true', help='Run in daemon mode')
    parser.add_argument('--dry-run', action='store_true', help='Enable dry run mode')
    parser.add_argument('--config', type=str, help='Path to config file')

    args = parser.parse_args()

    # Set dry run mode from command line if specified
    if args.dry_run:
        dry_run_manager.enabled = True

    # Create orchestrator
    orchestrator = Orchestrator()
    orchestrator.daemon = args.daemon

    # Add the FilesystemWatcher for bronze implementation
    filesystem_watcher = FilesystemWatcher()
    orchestrator.add_watcher(filesystem_watcher)

    print(f"AI Employee Orchestrator starting...")
    print(f"DRY_RUN mode: {is_dry_run()}")
    print(f"Vault path: {vault_manager.vault_path}")

    if args.daemon:
        print("Running in daemon mode...")
        orchestrator.start()
    else:
        print("Running single cycle...")

        # Process Claude tasks after running watchers
        print("Processing Claude tasks...")
        claude_interface.run_processing_cycle()

        orchestrator.run_once()

    print("AI Employee Orchestrator finished.")


if __name__ == "__main__":
    main()