from playwright.sync_api import sync_playwright
from pathlib import Path
import os
import sys

# Add project root to sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.env_manager import get_env
from src.vault.vault_manager import get_vault_manager

def run_auth():
    vault_manager = get_vault_manager()
    # Use the session directory specified by the user
    session_dir = vault_manager.vault_path / ".sessions" / "whatsapp"
    session_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Starting WhatsApp Auth with session dir: {session_dir}")
    print("Please scan the QR code in the browser window.")
    
    with sync_playwright() as p:
        # Launch browser in visible mode with modern User Agent and standard viewport
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(session_dir),
            headless=False,
            user_agent=user_agent,
            viewport={'width': 1280, 'height': 800},
            is_mobile=False,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        page = context.new_page()
        page.goto("https://web.whatsapp.com")
        
        print("\n" + "="*50)
        print("ACTION REQUIRED:")
        print("1. Scan the QR code if you are not logged in.")
        print("2. Wait for your chats to load.")
        print("3. ONCE LOADED, press ENTER here to save the session and close.")
        print("="*50 + "\n")
        
        input("Press Enter to finish and save session...")
        
        context.close()
        print(f"Session saved in {session_dir}. You can now run the WhatsApp watcher in headless mode.")

if __name__ == "__main__":
    run_auth()
