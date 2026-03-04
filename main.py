#!/usr/bin/env python3
"""
Main entry point for the Personal AI Employee System.
Integrates the Orchestrator and manages the lifecycle of the digital employee.
"""

import os
import sys
import argparse
from pathlib import Path

# Add the project root to the path so we can import modules correctly
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.orchestrator import Orchestrator
from src.watchers.filesystem_watcher import FilesystemWatcher
from src.watchers.gmail_watcher import GmailWatcher
from src.utils.dry_run import dry_run_manager, is_dry_run
from src.vault.vault_manager import vault_manager
from src.reasoning.claude_interface import claude_interface

def main():
    """Initialize and start the AI Employee system."""
    parser = argparse.ArgumentParser(description='Personal AI Employee System')
    parser.add_argument('--loop', action='store_true', help='Run in continuous loop mode (Silver Tier)')
    parser.add_argument('--dry-run', action='store_true', help='Enable dry run mode (default: from .env)')
    parser.add_argument('--agent-name', type=str, help='Name of this agent instance (Platinum Tier)')
    parser.add_argument('--agent-role', type=str, choices=['Cloud', 'Local'], help='Role of this agent (Platinum Tier)')
    
    args = parser.parse_args()

    # Apply command-line overrides
    if args.dry_run:
        dry_run_manager.enabled = True
    
    if args.agent_name:
        os.environ["AGENT_NAME"] = args.agent_name
        claude_interface.agent_name = args.agent_name
    
    if args.agent_role:
        os.environ["AGENT_ROLE"] = args.agent_role
        claude_interface.agent_role = args.agent_role
    
    agent_name = claude_interface.agent_name
    agent_role = claude_interface.agent_role

    print("="*50)
    print("PERSONAL AI EMPLOYEE SYSTEM - INITIALIZING")
    print("="*50)
    print(f"Agent Name: {agent_name}")
    print(f"Agent Role: {agent_role}")
    print(f"Vault Path: {vault_manager.vault_path}")
    print(f"Dry Run Mode: {is_dry_run()}")

    # Initialize Orchestrator
    orchestrator = Orchestrator()
    
    # Register Watchers based on Role
    # Cloud: Gmail, SocialMedia
    # Local: Filesystem, WhatsApp, Gmail (optional), SocialMedia (optional)
    
    print(f"\n[1/4] Initializing Filesystem Watcher...")
    if agent_role == 'Local':
        try:
            fs_watcher = FilesystemWatcher()
            orchestrator.add_watcher(fs_watcher)
            print(" -> Filesystem Watcher registered.")
        except Exception as e:
            print(f" !! Failed to initialize Filesystem Watcher: {e}")
    else:
        print(" -> Skipped (Role: Cloud)")

    print("[2/4] Initializing Gmail Watcher...")
    # Both can have it, but Cloud primarily owns triage
    try:
        gmail_watcher = GmailWatcher()
        orchestrator.add_watcher(gmail_watcher)
        print(" -> Gmail Watcher registered.")
    except Exception as e:
        print(f" !! Gmail Watcher skipped (Check credentials.json/token.json): {e}")

    print("[3/4] Initializing WhatsApp Watcher...")
    if agent_role == 'Local':
        try:
            from src.watchers.whatsapp_watcher import WhatsAppWatcher
            whatsapp_watcher = WhatsAppWatcher()
            orchestrator.add_watcher(whatsapp_watcher)
            print(" -> WhatsApp Watcher registered.")
        except Exception as e:
            print(f" !! WhatsApp Watcher skipped (Check playwright install): {e}")
    else:
        print(" -> Skipped (Role: Cloud owns Triage only)")

    print("[4/4] Initializing Social Media Watcher...")
    try:
        from src.watchers.social_media_watcher import SocialMediaWatcher
        social_media_watcher = SocialMediaWatcher()
        orchestrator.add_watcher(social_media_watcher)
        print(" -> Social Media Watcher registered.")
    except Exception as e:
        print(f" !! Social Media Watcher skipped: {e}")

    print("\n" + "="*50)
    if args.loop:
        print("STARTING SYSTEM IN LOOP MODE (Silver Tier)")
        print("Press Ctrl+C to shut down.")
        print("="*50 + "\n")
        orchestrator.start(loop=True)
    else:
        print("STARTING SYSTEM IN SINGLE-CYCLE MODE")
        print("="*50 + "\n")
        orchestrator.run_once()

    print("\n" + "="*50)
    print("AI EMPLOYEE SYSTEM SHUTDOWN COMPLETE")
    print("="*50)

if __name__ == "__main__":
    main()
