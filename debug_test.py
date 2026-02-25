#!/usr/bin/env python3
"""
Debug script to test the AI Employee System and see what's happening
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.vault.vault_manager import vault_manager
from src.reasoning.claude_interface import claude_interface
from src.watchers.filesystem_watcher import FilesystemWatcher

def debug_test():
    print("🔍 DEBUGGING THE AI EMPLOYEE SYSTEM")
    print("="*50)

    # Check vault directories
    print(f"\n📁 Vault Path: {vault_manager.vault_path}")

    # List files in each directory
    print(f"\n📥 Inbox files: {len(vault_manager.get_inbox_files())}")
    for f in vault_manager.get_inbox_files():
        print(f"   - {f.name}")

    print(f"\n📋 Needs_Action files: {len(vault_manager.get_needs_action_files())}")
    for f in vault_manager.get_needs_action_files():
        print(f"   - {f.name}")

    print(f"\n✅ Done files: {len(vault_manager.get_done_files())}")
    for f in vault_manager.get_done_files():
        print(f"   - {f.name}")

    print(f"\n📊 Vault stats: {vault_manager.get_vault_stats()}")

    # Now run the processing cycle
    print(f"\n🔄 Running Claude processing cycle...")
    claude_interface.run_processing_cycle()

    # Check again after processing
    print(f"\n📊 Vault stats after processing: {vault_manager.get_vault_stats()}")

    print(f"\n📥 Inbox files after processing: {len(vault_manager.get_inbox_files())}")
    for f in vault_manager.get_inbox_files():
        print(f"   - {f.name}")

    print(f"\n📋 Needs_Action files after processing: {len(vault_manager.get_needs_action_files())}")
    for f in vault_manager.get_needs_action_files():
        print(f"   - {f.name}")

    print(f"\n✅ Done files after processing: {len(vault_manager.get_done_files())}")
    for f in vault_manager.get_done_files():
        print(f"   - {f.name}")

    print(f"\n📋 Dashboard updated. Check Dashboard.md")

    print("\n✅ Debug test completed!")

if __name__ == "__main__":
    debug_test()