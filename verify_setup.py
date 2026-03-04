#!/usr/bin/env python3
"""
Verification script for the Personal AI Employee system vault structure.

This script checks that the necessary vault directories exist and are properly configured.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.vault.vault_manager import vault_manager

def verify_vault_structure():
    """Verify that all required vault directories exist."""
    print("🔍 Verifying vault structure...")
    print(f"Vault path: {vault_manager.vault_path}")

    # Define required directories
    required_dirs = [
        vault_manager.inbox_dir,
        vault_manager.needs_action_dir,
        vault_manager.done_dir,
        vault_manager.logs_dir
    ]

    all_good = True
    for directory in required_dirs:
        if directory.exists():
            print(f"✅ {directory.name}: OK")
        else:
            print(f"❌ {directory.name}: MISSING")
            all_good = False

    if all_good:
        print("\n✅ All vault directories are properly set up!")
    else:
        print("\n❌ Some vault directories are missing. The vault manager should create them automatically.")

    # Show current vault stats
    stats = vault_manager.get_vault_stats()
    print(f"\n📊 Current vault statistics:")
    for directory, count in stats.items():
        if directory != 'total_files' and directory != 'vault_path':
            print(f"  {directory}: {count} files")

    print(f"  total_files: {stats['total_files']}")

    return all_good

def verify_watchers():
    """Verify that watchers can be imported and instantiated."""
    print("\n🔍 Verifying watchers...")

    try:
        from src.watchers.filesystem_watcher import FilesystemWatcher
        fs_watcher = FilesystemWatcher()
        print("✅ FilesystemWatcher: OK")
        del fs_watcher  # Clean up
    except Exception as e:
        print(f"❌ FilesystemWatcher: {e}")

    try:
        from src.watchers.gmail_watcher import GmailWatcher
        # Do not initialize - this would trigger OAuth flow
        print("✅ GmailWatcher: Module imported successfully")
    except ImportError as e:
        print(f"❌ GmailWatcher: Import failed - {e}")
    except Exception as e:
        print(f"⚠️ GmailWatcher: Module available but has runtime dependencies - {e}")

def verify_skills():
    """Verify that agent skills are properly set up."""
    print("\n🔍 Verifying agent skills...")

    try:
        from src.skills.agent_skills import skill_registry
        skills = skill_registry.list_skills()
        print(f"✅ Agent Skills: OK - Found {len(skills)} skills")
        print(f"  Available skills: {', '.join(skills)}")
    except Exception as e:
        print(f"❌ Agent Skills: {e}")

def verify_google_libraries():
    """Verify that Google API libraries are available."""
    print("\n🔍 Verifying Google API libraries...")

    try:
        import googleapiclient
        import google.auth
        import google.auth.transport.requests
        import google.oauth2.credentials
        print("✅ Google API libraries: OK")
    except ImportError as e:
        print(f"❌ Google API libraries: Not installed - {e}")
        print("   Run: pip install -r requirements.txt")
    except Exception as e:
        print(f"⚠️ Google API libraries: Error - {e}")

if __name__ == "__main__":
    print("🛡️ Personal AI Employee - System Verification")
    print("=" * 50)

    verify_vault_structure()
    verify_watchers()
    verify_skills()
    verify_google_libraries()

    print("\n" + "=" * 50)
    print("📋 Verification complete!")