# Gmail Watcher Setup Instructions

## Prerequisites

To use the Gmail Watcher functionality in your Personal AI Employee system, you'll need to set up Google API credentials. Follow these steps carefully:

## Step 1: Enable Gmail API in Google Cloud Console

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. In the search bar, type "Gmail API" and select it from the results
4. Click "Enable" to enable the Gmail API for your project

## Step 2: Create Credentials

1. Go to the "Credentials" page in your Google Cloud Console
2. Click "Create Credentials" and select "OAuth client ID"
3. If prompted to configure the OAuth consent screen, do so first:
   - Choose "External" user type
   - Add your email to test users
4. For application type, select "Desktop application"
5. Give it a name like "Personal AI Employee Gmail Watcher"
6. Click "Create"
7. Download the credentials JSON file
8. Rename the downloaded file to `credentials.json`
9. Place the `credentials.json` file in your project root directory (same level as `src/`)

## Step 3: Install Required Dependencies

The project uses `uv` for dependency management. Install the required Google libraries:

```bash
# First, install uv if you don't have it
pip install uv

# Install the required dependencies
uv pip install -r requirements.txt
```

Alternatively, if you prefer pip:
```bash
pip install -r requirements.txt
```

## Step 4: Run the System

When you run the system for the first time, it will guide you through the OAuth flow:

1. Execute the orchestrator:
```bash
python src/orchestrator.py
```

2. On first run, you'll be prompted to authenticate:
   - A browser window will open
   - Sign in to your Google account
   - Grant permission for the app to read your Gmail
   - The authentication token will be saved for future use

## Step 5: Configure Email Monitoring

The Gmail Watcher is configured to look for emails that are both "unread" and "important". You can customize this by modifying the query in `src/watchers/gmail_watcher.py`.

## Troubleshooting

### Common Issues:

1. **"credentials.json not found"**: Ensure the credentials.json file is in the project root directory.

2. **"OAuth2 credentials have been revoked"**: Delete the `~/.credentials/gmail_token.json` file and run the system again to re-authenticate.

3. **"Access not configured"**: Make sure you've enabled the Gmail API in your Google Cloud Console project.

4. **"API has not been used in project"**: Double-check that the Gmail API is enabled and your credentials are valid.

### OAuth Scope:
The system requests the `https://www.googleapis.com/auth/gmail.readonly` scope, which allows read-only access to your Gmail account.

## Security Notes

- Keep your `credentials.json` file secure and do not commit it to version control
- The OAuth tokens are stored in `~/.credentials/gmail_token.json` in your home directory
- The application can only read your emails, not send them