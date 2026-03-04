#!/usr/bin/env python3
"""
Setup Gmail Authentication for AI Employee System
"""

import sys
from pathlib import Path
import os

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_gmail_auth():
    print("🔐 Gmail Authentication Setup for AI Employee System")
    print("="*60)

    # Check if Google libraries are available
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import Flow
    except ImportError:
        print("❌ Google libraries not installed!")
        print("Run: pip install -r requirements.txt")
        return False

    # Set environment
    os.environ['VAULT_PATH'] = 'AI_Employee_Vault'
    os.environ['DRY_RUN'] = 'false'

    # Check for credentials file
    credentials_path = Path('credentials.json')
    if not credentials_path.exists():
        print("❌ credentials.json file not found in project root!")
        print("Please follow the Gmail setup guide to create this file.")
        return False

    print(f"✅ Found credentials.json at: {credentials_path}")

    # Create token directory
    token_path = Path.home() / '.credentials' / 'gmail_token.json'

    print(f"Looking for existing token at: {token_path}")

    if token_path.exists():
        print("✅ Found existing token, no need to re-authenticate")
        return True

    print("\n⚠️ No existing token found, need to authenticate...")

    # Create the flow for WSL environment
    flow = Flow.from_client_secrets_file(
        str(credentials_path),
        scopes=['https://www.googleapis.com/auth/gmail.readonly'],
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # Out-of-band for WSL
    )

    # Get authorization URL
    auth_url, _ = flow.authorization_url(prompt='consent')

    print("\n📋 Follow these steps to complete authentication:")
    print("")
    print("1. Open this URL in your browser:")
    print(f"   {auth_url}")
    print("")
    print("2. Sign in to your Google account")
    print("3. Grant permission to read your Gmail")
    print("4. Copy the authorization code you receive")
    print("")

    # For WSL, we'll use a different approach - just get the code from user
    print("After completing step 4 above, come back here and continue...")
    input("Press Enter when you have the authorization code: ")

    print("\nNow we'll complete the authentication in a separate script...")

    # Write a temporary script to handle the token exchange
    temp_script = f"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

# Recreate the flow
flow = Flow.from_client_secrets_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/gmail.readonly'],
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)

print("Enter the authorization code you received:")
code = input().strip()

try:
    # Exchange the code for credentials
    flow.fetch_token(code=code)
    creds = flow.credentials

    # Create token directory and save credentials
    token_path = Path.home() / '.credentials' / 'gmail_token.json'
    token_path.parent.mkdir(parents=True, exist_ok=True)

    with open(token_path, 'w') as token:
        token.write(creds.to_json())

    print(f"✅ OAuth token saved successfully to: {{token_path}}")
    print("✅ Gmail authentication is now complete!")
    print("✅ You can now run the AI Employee system!")

except Exception as e:
    print(f"❌ Error completing authentication: {{e}}")
    import traceback
    traceback.print_exc()
"""

    # Write and execute the temporary script
    temp_file = Path('.temp_oauth_setup.py')
    with open(temp_file, 'w') as f:
        f.write(temp_script)

    print(f"\nExecuting authentication script...")
    print("Please run: python {temp_file}")
    print("Then enter your authorization code when prompted.")

    return True


if __name__ == "__main__":
    setup_gmail_auth()