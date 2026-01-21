# Quick Setup Checklist ✅

Use this checklist alongside OAUTH_SETUP_GUIDE.md to track your progress.

## Pre-Setup
- [ ] I have a Google account
- [ ] I have a Microsoft/Outlook account
- [ ] I have access to a Slack workspace
- [ ] I have a text editor ready

---

## Google Setup (15 min)

- [ ] Opened https://console.cloud.google.com/
- [ ] Created new project "Personal Dashboard"
- [ ] Enabled Gmail API
- [ ] Enabled Google Calendar API
- [ ] Enabled Google Docs API
- [ ] Configured OAuth consent screen (External)
- [ ] Added myself as test user
- [ ] Created OAuth Client ID (Web application)
- [ ] Added redirect URI: `http://localhost:5000/auth/google/callback`
- [ ] Downloaded credentials JSON
- [ ] Renamed to `google_credentials.json`
- [ ] Moved to `credentials/` folder
- [ ] Copied my Google Doc ID from the URL

**My Google Doc ID:** `_______________________________________`

---

## Microsoft Setup (15 min)

- [ ] Opened https://portal.azure.com/
- [ ] Navigated to App Registrations
- [ ] Created new registration "Personal Dashboard"
- [ ] Selected "Personal Microsoft accounts" option
- [ ] Added redirect URI: `http://localhost:5000/auth/microsoft/callback`
- [ ] Copied Application (client) ID
- [ ] Created new client secret
- [ ] Copied secret VALUE (not ID)
- [ ] Added API permission: Mail.Read
- [ ] Added API permission: Calendars.Read

**My Microsoft Client ID:** `_______________________________________`

**My Microsoft Secret:** `_______________________________________`

---

## Slack Setup (10 min)

- [ ] Opened https://api.slack.com/apps
- [ ] Created new app "Personal Dashboard" (From scratch)
- [ ] Selected my workspace
- [ ] Added redirect URL: `http://localhost:5000/auth/slack/callback`
- [ ] Added scope: channels:history
- [ ] Added scope: channels:read
- [ ] Added scope: groups:history
- [ ] Added scope: groups:read
- [ ] Added scope: im:history
- [ ] Added scope: mpim:history
- [ ] Added scope: search:read
- [ ] Added scope: users:read
- [ ] Copied Client ID
- [ ] Copied Client Secret

**My Slack Client ID:** `_______________________________________`

**My Slack Secret:** `_______________________________________`

---

## Configuration

- [ ] Copied `.env.example` to `.env`
- [ ] Generated random FLASK_SECRET_KEY
- [ ] Added GOOGLE_DOC_ID
- [ ] Added MICROSOFT_CLIENT_ID
- [ ] Added MICROSOFT_CLIENT_SECRET
- [ ] Added SLACK_CLIENT_ID
- [ ] Added SLACK_CLIENT_SECRET
- [ ] Saved and closed `.env`
- [ ] Verified `credentials/google_credentials.json` exists

---

## Installation

- [ ] Created virtual environment: `python3 -m venv venv`
- [ ] Activated venv: `source venv/bin/activate`
- [ ] Installed dependencies: `pip install -r requirements.txt`

---

## First Run

- [ ] Started server: `python app.py`
- [ ] Opened browser to http://localhost:5000
- [ ] Clicked "🔐 Authenticate" button
- [ ] Connected Google account
- [ ] Connected Microsoft account
- [ ] Connected Slack account
- [ ] Saw data appear on dashboard!

---

## 🎉 Success!

If all boxes are checked, you're done! Your dashboard should now be:
- Showing flagged emails from Gmail and Outlook
- Displaying upcoming calendar events
- Tracking Slack mentions
- Pulling to-dos from your Google Doc
- Auto-refreshing every 5 minutes

Enjoy your productivity dashboard! 🚀

---

## Troubleshooting

If something didn't work, check:
- [ ] All credentials in `.env` are correct (no typos)
- [ ] All redirect URIs are exactly: `http://localhost:5000/auth/[service]/callback`
- [ ] `credentials/google_credentials.json` file exists and is valid JSON
- [ ] All required APIs are enabled in Google Cloud Console
- [ ] All required permissions are granted in Azure and Slack
- [ ] Browser console (F12) for JavaScript errors
- [ ] Python console for error messages
