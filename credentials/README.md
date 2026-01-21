# Credentials Directory

Place your OAuth credential files here.

## Required Files

### google_credentials.json
Download this from Google Cloud Console after creating OAuth credentials.

**How to get it:**
1. Go to https://console.cloud.google.com/
2. Create/select a project
3. Enable Gmail API, Calendar API, and Docs API
4. Create OAuth 2.0 Client ID (Web application)
5. Add redirect URI: `http://localhost:5000/auth/google/callback`
6. Download the credentials JSON file
7. Rename it to `google_credentials.json` and place it here

## Optional Files

You can also store other credential files here if needed, though most other services use credentials stored in the `.env` file.

## Security

⚠️ **Never commit this directory to version control!**

The `.gitignore` file is already configured to exclude:
- `*.json` files in this directory
- `credentials.json`
- The entire `tokens/` directory

Your credentials are private and should stay on your local machine only.
