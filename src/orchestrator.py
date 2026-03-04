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
from src.watchers.gmail_watcher import GmailWatcher
from src.reasoning.claude_interface import claude_interface


class Orchestrator:
    """Main orchestrator for the AI Employee system."""

    def __init__(self):
        """Initialize the orchestrator."""
        self.watchers: List[BaseWatcher] = []
        self.running = False
        self.is_loop_mode = False

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
                # In loop mode, always start in a separate thread so multiple watchers can coexist
                if self.is_loop_mode:
                    watcher.start_daemon()
                else:
                    # In run-once mode, start() might block, but run_once() is usually preferred
                    # This is just a fallback for start() when not in loop mode
                    watcher.run_once()

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

    def process_approved_actions(self):
        """Process all files in the Approved directory and execute actions via MCP."""
        approved_files = vault_manager.get_approved_files()
        
        for file_path in approved_files:
            log_action(
                f"Processing approved action: {file_path.name}",
                actor="system",
                result="info",
                dry_run=is_dry_run()
            )
            
            content = vault_manager.read_file(file_path)
            if not content:
                continue

            # Platinum Tier: Role check
            # Local agent handles final execution of sensitive actions
            agent_role = get_env("AGENT_ROLE", "Local")
            
            # Simple logic to determine what to do
            action_executed = False
            
            if "email" in content.lower():
                # Execute email sending via MCP
                from src.mcp.mcp_servers.email_mcp import get_email_mcp
                email_mcp = get_email_mcp()
                # Simulate extracting it
                email_mcp.send_email(
                    to="recipient@example.com",
                    subject=f"RE: {file_path.name}",
                    body="Approved response content."
                )
                action_executed = True
            
            elif "odoo" in content.lower() and "post" in content.lower():
                # Execute Odoo posting
                from src.mcp.mcp_servers.odoo_mcp import get_odoo_mcp
                odoo_mcp = get_odoo_mcp()
                
                # Extract Invoice ID (simple regex or heuristic)
                import re
                match = re.search(r"Invoice ID: (\d+)", content)
                if match:
                    invoice_id = int(match.group(1))
                    odoo_mcp.post_invoice(invoice_id)
                    action_executed = True
            
            elif "social" in content.lower():
                # Execute social media posting
                from src.mcp.mcp_servers.social_mcp import get_social_mcp
                social_mcp = get_social_mcp()
                
                # Simple heuristic to determine platform and content
                platform = "Twitter"
                if "facebook" in content.lower(): platform = "Facebook"
                elif "instagram" in content.lower(): platform = "Instagram"
                
                # Execute via Playwright
                if platform == "Twitter":
                    social_mcp.post_to_twitter(content="Approved social content.")
                elif platform == "Facebook":
                    social_mcp.post_to_facebook(content="Approved social content.")
                else:
                    social_mcp.post_to_instagram(content="Approved social content.")
                
                log_action(f"Social Media: Executed approved post to {platform}", actor="system", result="success")
                action_executed = True

            if action_executed:
                # Move to Done
                vault_manager.move_to_done(file_path)
                log_action(
                    f"Approved action executed and moved to Done: {file_path.name}",
                    actor="system",
                    result="success"
                )
            else:
                log_action(
                    f"Approved file {file_path.name} did not match any execution logic",
                    actor="system",
                    result="warning"
                )

    def start(self, loop=False):
        """Start the orchestrator and all watchers."""
        if self.running:
            print("Orchestrator already running")
            return

        self.running = True
        self.is_loop_mode = loop
        
        log_action(
            "Starting AI Employee orchestrator",
            actor="system",
            result="success",
            details={"watcher_count": len(self.watchers), "loop_mode": loop},
            dry_run=is_dry_run()
        )

        # Update dashboard
        vault_manager.create_initial_dashboard()

        # Start all watchers
        self.start_watchers()

        print(f"Orchestrator started with {len(self.watchers)} watchers")
        print(f"DRY_RUN mode: {is_dry_run()}")
        print(f"Vault path: {vault_manager.vault_path}")

        # Keep the main thread alive if running in loop mode
        if self.is_loop_mode:
            print("Running in LOOP mode. Press Ctrl+C to stop.")
            last_sync_time = 0
            sync_interval = 300 # Sync every 5 minutes
            
            try:
                while self.running:
                    time.sleep(5)
                    # Process Claude tasks periodically
                    from src.reasoning.claude_interface import claude_interface
                    claude_interface.run_processing_cycle()
                    
                    # Process approved actions
                    self.process_approved_actions()

                    # Platinum Tier: Periodic Vault Sync
                    current_time = time.time()
                    if current_time - last_sync_time > sync_interval:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Orchestrator: Performing vault sync...")
                        success = vault_manager.vault_sync()
                        if not success:
                            log_action(
                                "CRITICAL: Cloud-Local sync is broken",
                                actor="system",
                                result="error",
                                details={"reason": "Git sync failed"}
                            )
                            # Create an alert file in the vault
                            alert_path = vault_manager.logs_dir / "sync_broken_alert.md"
                            vault_manager.write_file(alert_path, f"# SYNC BROKEN ALERT\n\nDetected at: {datetime.now().isoformat()}\n\nPlease check Git status and connectivity.")
                        last_sync_time = current_time

                    # Update dashboard periodically
                    vault_manager.create_initial_dashboard()
            except KeyboardInterrupt:
                self.stop()
        else:
            print("Single cycle completed.")
            # Final sync before exit if not dry run
            vault_manager.vault_sync()
            self.stop()

    def stop(self):
        """Stop the orchestrator and all watchers."""
        if not self.running:
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
        """Run a single cycle of all watchers."""
        self.start(loop=False)


def main():
    """Main entry point for the orchestrator."""
    import argparse

    parser = argparse.ArgumentParser(description='AI Employee Orchestrator')
    parser.add_argument('--loop', action='store_true', help='Run in continuous loop mode')
    parser.add_argument('--daemon', action='store_true', help='Alias for --loop')
    parser.add_argument('--dry-run', action='store_true', help='Enable dry run mode')
    parser.add_argument('--config', type=str, help='Path to config file')

    args = parser.parse_args()

    # Set dry run mode from command line if specified
    if args.dry_run:
        dry_run_manager.enabled = True

    # Create orchestrator
    orchestrator = Orchestrator()
    loop_mode = args.loop or args.daemon

    # Add the FilesystemWatcher for bronze implementation
    filesystem_watcher = FilesystemWatcher()
    orchestrator.add_watcher(filesystem_watcher)

    # Add the GmailWatcher if Google libraries are available
    try:
        gmail_watcher = GmailWatcher()
        orchestrator.add_watcher(gmail_watcher)
        print("GmailWatcher initialized and added to orchestrator")
    except Exception as e:
        print(f"Could not initialize GmailWatcher: {e}")
        print("Make sure you have installed the required Google libraries and set up credentials.json")

    # Add the WhatsAppWatcher
    try:
        from src.watchers.whatsapp_watcher import WhatsAppWatcher
        whatsapp_watcher = WhatsAppWatcher()
        orchestrator.add_watcher(whatsapp_watcher)
        print("WhatsAppWatcher initialized and added to orchestrator")
    except Exception as e:
        print(f"Could not initialize WhatsAppWatcher: {e}")
        print("Make sure you have installed playwright and its dependencies.")

    # Add the SocialMediaWatcher
    try:
        from src.watchers.social_media_watcher import SocialMediaWatcher
        social_media_watcher = SocialMediaWatcher()
        orchestrator.add_watcher(social_media_watcher)
        print("SocialMediaWatcher initialized and added to orchestrator")
    except Exception as e:
        print(f"Could not initialize SocialMediaWatcher: {e}")

    print(f"AI Employee Orchestrator starting...")
    print(f"DRY_RUN mode: {is_dry_run()}")
    print(f"Vault path: {vault_manager.vault_path}")

    if loop_mode:
        orchestrator.start(loop=True)
    else:
        print("Running single cycle...")
        orchestrator.run_once()

    print("AI Employee Orchestrator finished.")


if __name__ == "__main__":
    main()