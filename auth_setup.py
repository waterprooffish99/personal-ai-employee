import sys
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

# Initialize the OAuth Flow
flow = Flow.from_client_secrets_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/gmail.readonly'],
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)

# Get the URL for the user to visit
auth_url, _ = flow.authorization_url(prompt='consent')
print(f'Please go to this URL and authorize: \n{auth_url}\n')

# Wait for user input
code = input('Enter the authorization code: ').strip()

try:
    flow.fetch_token(code=code)
    creds = flow.credentials

    token_path = Path.home() / '.credentials' / 'gmail_token.json'
    token_path.parent.mkdir(parents=True, exist_ok=True)

    with open(token_path, 'w') as token:
        token.write(creds.to_json())

    print(f'✅ OAuth token saved successfully to: {token_path}')
    print('✅ Gmail authentication is now complete!')
except Exception as e:
    print(f'❌ Error completing authentication: {e}')
