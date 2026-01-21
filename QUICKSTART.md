# Quick Start Guide

Get your dashboard up and running in 10 minutes!

## Prerequisites
- Python 3.8+
- A Google account
- A Microsoft/Outlook account
- A Slack workspace (optional)

## Quick Setup (5 Steps)

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Set Up Google OAuth (Most Important)

This gives you Gmail, Google Calendar, and Google Docs access.

1. Go to: https://console.cloud.google.com/
2. Create a new project
3. Enable these APIs:
   - Gmail API
   - Google Calendar API
   - Google Docs API
4. Create OAuth credentials:
   - Type: Web application
   - Redirect URI: `http://localhost:5000/auth/google/callback`
5. Download the credentials JSON file
6. Save it as: `credentials/google_credentials.json`

### 3. Set Up Microsoft OAuth

This gives you Outlook email and calendar access.

1. Go to: https://portal.azure.com/
2. Azure AD > App registrations > New registration
3. Redirect URI: `http://localhost:5000/auth/microsoft/callback`
4. API Permissions: Mail.Read, Calendars.Read
5. Create a client secret
6. Copy Client ID and Secret

### 4. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env and add:
# - MICROSOFT_CLIENT_ID (from step 3)
# - MICROSOFT_CLIENT_SECRET (from step 3)
# - GOOGLE_DOC_ID (your to-do list doc ID from the URL)
```

The Google credentials are in the JSON file, so you don't need to add them to .env.

### 5. Run the Dashboard

```bash
# Create required directories
mkdir -p tokens

# Start the server
python app.py
```

Open http://localhost:5000 and click "🔐 Authenticate" to connect your accounts!

## Optional: Set Up Slack

1. Go to: https://api.slack.com/apps
2. Create new app
3. Add redirect URI: `http://localhost:5000/auth/slack/callback`
4. Add User Token Scopes: channels:history, search:read, etc.
5. Copy Client ID and Secret to .env

## That's It!

Your dashboard should now be running and pulling data from:
- Gmail (flagged emails)
- Google Calendar
- Google Docs (your to-do list)
- Outlook (flagged emails)
- Outlook Calendar
- Slack (if configured)

The dashboard auto-refreshes every 5 minutes. Enjoy!

## Troubleshooting

**"File not found" errors**: Make sure you created the `credentials/` and `tokens/` directories

**"Invalid credentials"**: Double-check your OAuth redirect URIs match exactly

**No data showing**: Make sure you have flagged emails or calendar events to display

**Port 5000 in use**: Change PORT in .env to 5001 or another free port

For detailed help, see README.md
