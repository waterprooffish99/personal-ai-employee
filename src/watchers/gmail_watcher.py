"""
Gmail Watcher for the AI Employee System.

This module implements a Gmail watcher that monitors for unread and important emails,
and creates action files in the vault when relevant emails are detected.
"""

import time
import email
import base64
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from .base_watcher import BaseWatcher
from ..vault.vault_manager import vault_manager, get_vault_manager
from ..utils.logger import log_action
from ..utils.dry_run import is_dry_run, execute_if_real

# Try to import Google API libraries - we'll check if they're available
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("Google API libraries not available. Gmail Watcher will not function until dependencies are installed.")


class GmailWatcher(BaseWatcher):
    """
    GmailWatcher monitors Gmail for unread and important emails and creates
    action files in the vault when relevant emails are found.
    """

    def __init__(self, poll_interval: int = 60):
        """
        Initialize the GmailWatcher.

        Args:
            poll_interval: Interval in seconds between checks (default 60)
        """
        super().__init__("GmailWatcher", poll_interval)

        if not GOOGLE_AVAILABLE:
            log_action(
                "Google API libraries not available for GmailWatcher",
                actor="system",
                result="warning",
                details={"error": "google-api-python-client and google-auth libraries not installed"},
                dry_run=is_dry_run()
            )

        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google API using credentials.json."""
        if not GOOGLE_AVAILABLE:
            return

        creds = None
        # The file token.json stores the user's access and refresh tokens.
        token_path = Path.home() / ".credentials" / "gmail_token.json"
        credentials_path = Path("credentials.json")

        # Check for credentials in multiple locations
        possible_creds_paths = [
            Path("credentials.json"),
            Path.home() / ".credentials" / "credentials.json",
            Path("src") / "credentials.json",
            Path(".") / "credentials.json"
        ]

        creds_file = None
        for path in possible_creds_paths:
            if path.exists():
                creds_file = path
                break

        if not creds_file:
            log_action(
                "No credentials.json file found for Gmail authentication",
                actor="system",
                result="error",
                details={"suggestion": "Create credentials.json from Google Cloud Console"},
                dry_run=is_dry_run()
            )
            return

        try:
            # Load existing token if available
            if token_path.exists():
                creds = Credentials.from_authorized_user_file(str(token_path),
                                                              scopes=['https://www.googleapis.com/auth/gmail.readonly'])

            # If there are no valid credentials available, request authorization
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Use the found credentials file
                    flow = Flow.from_client_secrets_file(
                        str(creds_file),
                        scopes=['https://www.googleapis.com/auth/gmail.readonly'],
                        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
                    )
                    flow.run_local_server(port=0)
                    creds = flow.credentials

                # Save the credentials for the next run
                token_path.parent.mkdir(parents=True, exist_ok=True)
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())

            # Build the Gmail service
            self.service = build('gmail', 'v1', credentials=creds)

            log_action(
                "Gmail authentication successful",
                actor="system",
                result="success",
                dry_run=is_dry_run()
            )
        except Exception as e:
            log_action(
                "Failed to authenticate with Gmail API",
                actor="system",
                result="error",
                details={"error": str(e)},
                dry_run=is_dry_run()
            )

    def check_for_updates(self) -> bool:
        """
        Check for unread and important emails in Gmail.

        Returns:
            True if new emails were detected, False otherwise
        """
        if not GOOGLE_AVAILABLE or not self.service:
            log_action(
                "Gmail service not available, skipping check",
                actor="system",
                result="warning",
                dry_run=is_dry_run()
            )
            return False

        try:
            # Query for unread emails - you can customize this query
            query = 'is:unread is:important'
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=10  # Limit to last 10 unread important emails
            ).execute()

            messages = results.get('messages', [])
            new_emails_detected = False

            for msg in messages:
                # Get the full message
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg['id']
                ).execute()

                # Process the email
                processed = self._process_email_message(message)
                if processed:
                    new_emails_detected = True

            return new_emails_detected
        except Exception as e:
            log_action(
                "Error checking for Gmail updates",
                actor="system",
                result="error",
                details={"error": str(e)},
                dry_run=is_dry_run()
            )
            return False

    def _process_email_message(self, message: Dict[str, Any]) -> bool:
        """
        Process a Gmail message and create an action file in the vault.

        Args:
            message: Gmail message object

        Returns:
            True if successfully processed, False otherwise
        """
        try:
            # Extract email headers
            headers = {header['name']: header['value'] for header in message['payload']['headers']}

            # Get basic email information
            sender = headers.get('From', 'Unknown Sender')
            subject = headers.get('Subject', 'No Subject')
            received_date = headers.get('Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            # Get email body
            body = self._get_email_body(message)

            # Create the action file with required schema
            action_filename = f"email_{int(time.time())}_{sender.split('@')[0]}.md"
            action_path = vault_manager.needs_action_dir / action_filename

            # Create action content with YAML frontmatter as specified
            action_content = f"""---
type: email
from: "{sender}"
subject: "{subject}"
received: "{received_date}"
---

# Email from {sender}

**Subject**: {subject}

**Received**: {received_date}

## Email Content:
{body}

---
This email was marked as important and requires your attention.
Please process this email and move the file to the Done directory when completed.
"""

            # Write the action file
            success = vault_manager.write_file(action_path, action_content)

            if success:
                log_action(
                    f"Created action file for email from {sender}",
                    actor="system",
                    result="success",
                    details={
                        "subject": subject,
                        "action_file": str(action_path),
                        "sender": sender
                    },
                    dry_run=is_dry_run()
                )
                return True
            else:
                log_action(
                    f"Failed to create action file for email from {sender}",
                    actor="system",
                    result="error",
                    details={"subject": subject, "sender": sender},
                    dry_run=is_dry_run()
                )
                return False

        except Exception as e:
            log_action(
                f"Error processing email message",
                actor="system",
                result="error",
                details={"error": str(e)},
                dry_run=is_dry_run()
            )
            return False

    def _get_email_body(self, message: Dict[str, Any]) -> str:
        """
        Extract the body content from a Gmail message.

        Args:
            message: Gmail message object

        Returns:
            The email body content as a string
        """
        try:
            # Check if the message has a body
            if 'body' in message['payload']:
                body_data = message['payload']['body']
                if 'data' in body_data:
                    # Decode the base64 encoded body
                    body = base64.urlsafe_b64decode(body_data['data']).decode('utf-8')
                    return body

            # If no body in the main payload, look in the parts
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body_data = part['body']
                        if 'data' in body_data:
                            body = base64.urlsafe_b64decode(body_data['data']).decode('utf-8')
                            return body

            # If no text/plain part, try to get the first available part
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part.get('mimeType', '').startswith('text/'):
                        body_data = part['body']
                        if 'data' in body_data:
                            body = base64.urlsafe_b64decode(body_data['data']).decode('utf-8')
                            return body

            return "Email body could not be extracted."

        except Exception as e:
            log_action(
                f"Error extracting email body: {str(e)}",
                actor="system",
                result="error",
                dry_run=is_dry_run()
            )
            return "Email body could not be extracted due to an error."