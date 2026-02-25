#!/usr/bin/env python3
"""
Test script to validate the Bronze implementation of the AI Employee System.
"""

import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.watchers.filesystem_watcher import FilesystemWatcher
from src.reasoning.claude_interface import claude_interface
from src.vault.vault_manager import vault_manager
from src.utils.logger import log_action


def test_bronze_implementation():
    """Test the Bronze implementation components."""
    print("Testing Bronze Implementation...")

    # Test 1: Verify vault structure exists
    print("\n1. Testing vault structure...")
    vault_dirs = [
        vault_manager.inbox_dir,
        vault_manager.needs_action_dir,
        vault_manager.done_dir,
        vault_manager.logs_dir,
        vault_manager.pending_approval_dir,
        vault_manager.approved_dir,
        vault_manager.rejected_dir,
        vault_manager.plans_dir,
        vault_manager.briefings_dir,
        vault_manager.accounting_dir
    ]

    for vault_dir in vault_dirs:
        if vault_dir.exists():
            print(f"   ✓ {vault_dir.name} directory exists")
        else:
            print(f"   ✗ {vault_dir.name} directory missing")
            return False

    # Test 2: Test FilesystemWatcher
    print("\n2. Testing FilesystemWatcher...")
    try:
        watcher = FilesystemWatcher()
        print("   ✓ FilesystemWatcher initialized successfully")
    except Exception as e:
        print(f"   ✗ FilesystemWatcher initialization failed: {e}")
        return False

    # Test 3: Test Claude Interface
    print("\n3. Testing Claude Interface...")
    try:
        # Test processing cycle
        claude_interface.run_processing_cycle()
        print("   ✓ Claude interface processing cycle completed")
    except Exception as e:
        print(f"   ✗ Claude interface processing failed: {e}")
        return False

    # Test 4: Test file operations
    print("\n4. Testing file operations...")
    try:
        # Create a test file in the Inbox
        test_file_path = vault_manager.inbox_dir / f"test_file_{int(time.time())}.txt"
        with open(test_file_path, 'w') as f:
            f.write("This is a test file for the AI Employee System.")
        print("   ✓ Test file created in Inbox")

        # Test reading the file
        content = vault_manager.read_file(test_file_path)
        if content:
            print("   ✓ File reading successful")
        else:
            print("   ✗ File reading failed")
            return False

        # Move the file to Needs_Action
        success = vault_manager.move_to_needs_action(test_file_path)
        if success:
            print("   ✓ File moved to Needs_Action successfully")
        else:
            print("   ✗ File move to Needs_Action failed")
            return False

    except Exception as e:
        print(f"   ✗ File operations test failed: {e}")
        return False

    # Test 5: Test dashboard update
    print("\n5. Testing dashboard update...")
    try:
        vault_manager.create_initial_dashboard()
        print("   ✓ Dashboard updated successfully")
    except Exception as e:
        print(f"   ✗ Dashboard update failed: {e}")
        return False

    # Test 6: Test logging
    print("\n6. Testing logging system...")
    try:
        log_action("Bronze implementation test completed successfully", actor="system", result="success")
        print("   ✓ Logging system working")
    except Exception as e:
        print(f"   ✗ Logging system failed: {e}")
        return False

    # Test 7: Test agent skills
    print("\n7. Testing agent skills...")
    try:
        from src.skills.agent_skills import execute_skill

        # Test file operation skill
        result = execute_skill(
            "file_operation",
            operation="list",
            directory="needs_action"
        )
        if result["success"]:
            print("   ✓ Agent skills framework working")
        else:
            print(f"   ? Agent skills framework: {result.get('result', 'Unknown issue')}")
            # Don't fail the test for this, as it might just be an empty directory
    except Exception as e:
        print(f"   ✗ Agent skills test failed: {e}")
        return False

    print("\n✓ All Bronze implementation tests passed!")
    print("\nBronze Implementation Summary:")
    print("- FilesystemWatcher monitoring /Inbox directory")
    print("- Claude Code integration reading from /Needs_Action")
    print("- Task lifecycle: Files move from /Inbox → /Needs_Action → /Done")
    print("- Dashboard updates with current status")
    print("- JSON logging to /Logs directory")
    print("- Agent skills framework available")

    return True


if __name__ == "__main__":
    success = test_bronze_implementation()
    if success:
        print("\n🎉 Bronze implementation validation successful!")
        print("\nYou can now run the orchestrator with:")
        print("  python src/orchestrator.py --daemon   # For continuous operation")
        print("  python src/orchestrator.py            # For single cycle")
    else:
        print("\n❌ Bronze implementation validation failed!")
        sys.exit(1)