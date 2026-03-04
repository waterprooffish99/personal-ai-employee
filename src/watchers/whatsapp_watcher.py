from playwright.sync_api import sync_playwright
from pathlib import Path
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import os

from .base_watcher import BaseWatcher
from ..utils.env_manager import get_env
from ..utils.logger import log_action
from ..utils.dry_run import is_dry_run
from ..vault.vault_manager import get_vault_manager

class WhatsAppWatcher(BaseWatcher):
    """Monitor WhatsApp Web for specific keywords and create tasks in the vault."""

    def __init__(self, name: str = "whatsapp_watcher", poll_interval: int = 60, keywords: List[str] = None):
        """
        Initialize the WhatsApp watcher.

        Args:
            name: Name of the watcher
            poll_interval: Interval in seconds between checks
            keywords: List of keywords to monitor for
        """
        super().__init__(name, poll_interval)
        self.keywords = keywords or ["urgent", "invoice", "payment", "due", "critical", "asap"]
        self.vault_manager = get_vault_manager()
        # Use the same session directory as the auth script
        self.session_dir = self.vault_manager.vault_path / ".sessions" / "whatsapp"
        self.browser_context = None
        self.browser = None
        self.playwright = None
        self.page = None

    def _setup_browser(self):
        """Setup Playwright browser with persistent context."""
        if self.page:
            return

        self.playwright = sync_playwright().start()
        
        # Ensure session directory exists
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        # Use a modern, common User Agent and standard viewport
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        
        self.browser_context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.session_dir),
            headless=True,
            user_agent=user_agent,
            viewport={'width': 1280, 'height': 800},
            is_mobile=False,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        self.page = self.browser_context.new_page()
        self.page.goto("https://web.whatsapp.com")
        
        # Wait for WhatsApp to load (Increased timeout to 100s for WSL stability)
        try:
            # First, wait for any "Syncing..." or "Loading..." overlay to disappear if it exists
            try:
                self.page.wait_for_selector('div[aria-label*="Loading"]', timeout=5000)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] WhatsAppWatcher: Detected 'Loading' overlay, waiting for sync...")
                # Wait for it to disappear
                self.page.wait_for_selector('div[aria-label*="Loading"]', state="hidden", timeout=60000)
            except:
                pass # No loading overlay detected or it went away fast

            # Mandatory wait for chat list
            self.page.wait_for_selector('[data-testid="chat-list"], [role="grid"], [aria-label="Chat list"]', timeout=100000)
            
            # Additional settling time to let the list fully render
            print(f"[{datetime.now().strftime('%H:%M:%S')}] WhatsAppWatcher: Chat list detected. Settling for 10 seconds...")
            time.sleep(10)

            log_action(
                "WhatsApp Web loaded successfully",
                actor="system",
                result="success"
            )
        except Exception as e:
            log_action(
                "WhatsApp Web did not load correctly",
                actor="system",
                result="warning",
                details={"error": str(e)}
            )
            # Save debug screenshot to vault logs
            debug_path = self.vault_manager.logs_dir / "debug_whatsapp_error.png"
            self.page.screenshot(path=str(debug_path))
            log_action(
                f"Saved error screenshot to {debug_path}",
                actor="system",
                result="info"
            )

    def check_for_updates(self) -> bool:
        """
        Check for new messages matching the keywords.
        """
        try:
            self._setup_browser()
            
            if not self.page:
                return False

            # Take a debug screenshot every check
            debug_path = self.vault_manager.logs_dir / "debug_whatsapp.png"
            self.page.screenshot(path=str(debug_path))

            # Find all chat containers - WhatsApp often uses 'cell-frame-container' 
            # or 'list-item' based on the version. Added simpler selectors.
            chat_containers = self.page.query_selector_all('[data-testid="cell-frame-container"], [role="listitem"], [role="row"]')
            
            unread_count = 0
            new_events = False
            
            for container in chat_containers:
                # Aggressive unread check: Search for any element with aria-label containing "unread"
                # This covers both the green circle and the unread message count
                unread_indicator = container.query_selector('[aria-label*="unread"], [data-testid*="unread"]')
                
                if unread_indicator:
                    unread_count += 1
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] WhatsAppWatcher: I see a green circle!")
                    
                    # Read the snippet text and convert to lowercase for case-insensitive matching
                    text = container.inner_text().lower()
                    
                    found_keywords = [k.lower() for k in self.keywords if k.lower() in text]
                    if found_keywords:
                        # We found a match!
                        chat_name = "Unknown"
                        # Try multiple ways to find the chat name
                        name_el = container.query_selector('span[dir="auto"], [title]')
                        if name_el:
                            chat_name = name_el.inner_text() or name_el.get_attribute("title")
                        
                        self._create_task_file(chat_name, text, found_keywords)
                        new_events = True
            
            # Debug Log in terminal
            print(f"[{datetime.now().strftime('%H:%M:%S')}] WhatsAppWatcher: Checked {len(chat_containers)} chats, found {unread_count} unread. Screenshot: {debug_path.name}")
            
            return new_events

        except Exception as e:
            log_action(
                "Error checking WhatsApp updates",
                actor="system",
                result="error",
                details={"error": str(e)}
            )
            return False

    def _create_task_file(self, chat_name: str, message_text: str, keywords: List[str]):
        """Create a markdown file in /Needs_Action for the found message."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"whatsapp_{chat_name}_{timestamp}.md".replace(" ", "_")
        file_path = self.vault_manager.needs_action_dir / filename
        
        content = f"""# WhatsApp Message: {chat_name}

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Keywords Found**: {', '.join(keywords)}

## Message Content
{message_text}

## Required Action
A message from WhatsApp was flagged as urgent or containing important keywords. Please review and respond if necessary.

---
*Created by WhatsAppWatcher*
"""
        
        if is_dry_run():
            log_action(
                f"Would create task file for WhatsApp message from {chat_name}",
                actor="system",
                result="info",
                dry_run=True
            )
        else:
            self.vault_manager.write_file(file_path, content)
            log_action(
                f"Created task file for WhatsApp message from {chat_name}",
                actor="system",
                result="success",
                details={"file": filename}
            )

    def stop(self):
        """Clean up resources."""
        super().stop()
        if self.browser_context:
            self.browser_context.close()
        if self.playwright:
            self.playwright.stop()
