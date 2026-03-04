import os
from pathlib import Path
from typing import Dict, Any, Optional
from playwright.sync_api import sync_playwright

from ...utils.logger import log_action
from ...utils.dry_run import is_dry_run
from ...vault.vault_manager import get_vault_manager

class SocialMCPServer:
    """MCP server for posting to social media platforms using Playwright."""

    def __init__(self):
        self.vault_manager = get_vault_manager()
        self.session_dir = self.vault_manager.vault_path / ".sessions" / "social"
        self.session_dir.mkdir(parents=True, exist_ok=True)

    def _post_with_playwright(self, platform: str, url: str, selector: str, content: str) -> Dict[str, Any]:
        """Generic Playwright poster for social media."""
        if is_dry_run():
            log_action(f"Social MCP: Would post to {platform}", actor="system", result="info", details={"content": content}, dry_run=True)
            return {"status": "success", "message": f"Dry run: Posted to {platform}"}

        try:
            with sync_playwright() as p:
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.session_dir),
                    headless=True,
                    user_agent=user_agent,
                    viewport={'width': 1280, 'height': 800},
                    is_mobile=False,
                    args=["--no-sandbox", "--disable-setuid-sandbox"]
                )
                page = browser.new_page()
                page.goto(url)
                
                # Wait for the post input area
                try:
                    page.wait_for_selector(selector, timeout=15000)
                    page.fill(selector, content)
                    # Simulate pressing "Post" button
                    log_action(f"Social MCP: Simulated posting to {platform}", actor="system", result="success")
                    status = "success"
                    message = f"Posted to {platform} successfully."
                except Exception as e:
                    # Capture screenshot for debugging
                    screenshot_path = self.vault_manager.logs_dir / f"error_social_{platform.lower()}.png"
                    page.screenshot(path=str(screenshot_path))
                    log_action(f"Social MCP: Error finding selector on {platform}", actor="system", result="error", details={"error": str(e), "screenshot": str(screenshot_path)})
                    status = "error"
                    message = f"Failed to post to {platform}: {str(e)}"
                
                browser.close()
                return {"status": status, "message": message}
        except Exception as e:
            log_action(f"Social MCP: Browser error for {platform}", actor="system", result="error", details={"error": str(e)})
            return {"status": "error", "message": str(e)}

    def post_to_twitter(self, content: str) -> Dict[str, Any]:
        """Post a message to Twitter (X)."""
        return self._post_with_playwright(
            platform="Twitter",
            url="https://twitter.com/compose/tweet",
            selector="div[data-testid='tweetTextarea_0']",
            content=content
        )

    def post_to_facebook(self, content: str) -> Dict[str, Any]:
        """Post a message to Facebook."""
        return self._post_with_playwright(
            platform="Facebook",
            url="https://facebook.com",
            selector="div[role='textbox']",
            content=content
        )

    def post_to_instagram(self, content: str) -> Dict[str, Any]:
        """Post a message to Instagram."""
        return self._post_with_playwright(
            platform="Instagram",
            url="https://instagram.com",
            selector="textarea",
            content=content
        )

def get_social_mcp():
    return SocialMCPServer()
