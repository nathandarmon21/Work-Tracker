# Step-by-Step OAuth Setup Guide

This guide will walk you through setting up OAuth credentials for Google, Microsoft, and Slack. Follow each section carefully, and you'll be up and running in about 20-30 minutes.

---

## 📋 Prerequisites

Before starting, make sure you have:
- [ ] A Google account (Gmail)
- [ ] A Microsoft account (Outlook/Office 365)
- [ ] Access to a Slack workspace
- [ ] A text editor to edit the `.env` file

---

## 🔷 Part 1: Google OAuth Setup (15 minutes)

Google will give you access to Gmail, Google Calendar, and Google Docs.

### Step 1: Go to Google Cloud Console

1. Open your browser and go to: **https://console.cloud.google.com/**
2. Sign in with your Google account
3. You should see the Google Cloud Console dashboard

### Step 2: Create a New Project

1. Click the **project dropdown** at the top (it might say "Select a project")
2. Click **"NEW PROJECT"** in the top-right of the popup
3. Fill in the details:
   - **Project name**: `Personal Dashboard` (or any name you like)
   - **Organization**: Leave as "No organization"
4. Click **"CREATE"**
5. Wait a few seconds for the project to be created
6. Make sure your new project is selected in the dropdown

### Step 3: Enable Required APIs

You need to enable 3 APIs. For each one, follow these steps:

1. Click the **☰ hamburger menu** (top-left)
2. Navigate to: **APIs & Services** → **Library**
3. In the search bar, type the API name
4. Click on the API
5. Click the **"ENABLE"** button
6. Wait for it to enable (takes a few seconds)

**Enable these 3 APIs:**
- ✅ **Gmail API**
- ✅ **Google Calendar API**
- ✅ **Google Docs API**

### Step 4: Configure OAuth Consent Screen

1. Click **☰ menu** → **APIs & Services** → **OAuth consent screen**
2. Choose **"External"** (unless you have a Google Workspace account)
3. Click **"CREATE"**
4. Fill in the required fields:
   - **App name**: `Personal Dashboard`
   - **User support email**: Your email address
   - **Developer contact email**: Your email address
5. Scroll down and click **"SAVE AND CONTINUE"**
6. On the "Scopes" page, click **"SAVE AND CONTINUE"** (we'll add scopes later)
7. On the "Test users" page, click **"+ ADD USERS"**
8. Enter your Gmail address
9. Click **"ADD"**
10. Click **"SAVE AND CONTINUE"**
11. Review the summary and click **"BACK TO DASHBOARD"**

### Step 5: Create OAuth Credentials

1. Click **☰ menu** → **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"OAuth client ID"**
4. If prompted to configure consent screen, you've already done it - just continue
5. Fill in the details:
   - **Application type**: Select **"Web application"**
   - **Name**: `Personal Dashboard Web Client`
6. Under **"Authorized redirect URIs"**:
   - Click **"+ ADD URI"**
   - Enter exactly: `http://localhost:5000/auth/google/callback`
   - ⚠️ **Important**: Must be exact - no trailing slash, no https
7. Click **"CREATE"**

### Step 6: Download Credentials

1. A popup will show your Client ID and Client Secret
2. Click the **"DOWNLOAD JSON"** button (looks like ⬇️)
3. The file will download with a long name like `client_secret_XXXXX.json`
4. **Rename this file** to: `google_credentials.json`
5. **Move it** to the `credentials/` folder in your Work-Tracker directory:
   ```bash
   mv ~/Downloads/google_credentials.json /home/user/Work-Tracker/credentials/
   ```

### Step 7: Get Your Google Doc ID

If you want to track your Google Docs to-do list:

1. Open your Google Doc: https://docs.google.com/document/d/1dQSlBfc1Ptlqm31ZUuwT1KXKwe7LzR0qmO1sJSbOOeU/edit
2. Look at the URL - it has this format:
   ```
   https://docs.google.com/document/d/YOUR_DOC_ID_HERE/edit...
   ```
3. Copy the **YOUR_DOC_ID_HERE** part
4. In this case, it's: `1dQSlBfc1Ptlqm31ZUuwT1KXKwe7LzR0qmO1sJSbOOeU`
5. Save this - you'll add it to `.env` later

### ✅ Google Setup Complete!

You should now have:
- ✅ `credentials/google_credentials.json` file
- ✅ Google Doc ID (if using to-do tracking)

---

## 🔷 Part 2: Microsoft OAuth Setup (15 minutes)

Microsoft will give you access to Outlook email and calendar.

### Step 1: Go to Azure Portal

1. Open your browser and go to: **https://portal.azure.com/**
2. Sign in with your Microsoft account
3. You should see the Azure portal dashboard

### Step 2: Navigate to App Registrations

1. In the search bar at the top, type: **"App registrations"**
2. Click on **"App registrations"** in the results
3. Or navigate via: Azure Active Directory → App registrations

### Step 3: Register a New Application

1. Click **"+ New registration"** at the top
2. Fill in the details:
   - **Name**: `Personal Dashboard`
   - **Supported account types**: Select **"Accounts in any organizational directory and personal Microsoft accounts"**
     - This is the 3rd option that includes personal accounts
   - **Redirect URI**:
     - Select **"Web"** from the dropdown
     - Enter: `http://localhost:5000/auth/microsoft/callback`
3. Click **"Register"**

### Step 4: Copy Application (Client) ID

1. You'll be taken to the app overview page
2. Find **"Application (client) ID"** - it looks like: `12345678-1234-1234-1234-123456789abc`
3. Click the **copy icon** next to it
4. **Save this somewhere** - you'll need it for `.env`

### Step 5: Create a Client Secret

1. In the left sidebar, click **"Certificates & secrets"**
2. Click **"+ New client secret"**
3. Fill in:
   - **Description**: `Dashboard Secret`
   - **Expires**: Choose **"12 months"** (or your preference)
4. Click **"Add"**
5. **⚠️ IMPORTANT**: Copy the **Value** immediately (not the Secret ID)
   - It looks like a long random string
   - **You can only see this once** - it will be hidden after you leave this page
6. **Save this somewhere** - you'll need it for `.env`

### Step 6: Add API Permissions

1. In the left sidebar, click **"API permissions"**
2. You should see "User.Read" already listed
3. Click **"+ Add a permission"**
4. Click **"Microsoft Graph"**
5. Click **"Delegated permissions"**
6. In the search box, type: **"Mail"**
   - Expand **"Mail"**
   - Check **"Mail.Read"**
7. In the search box, type: **"Calendars"**
   - Expand **"Calendars"**
   - Check **"Calendars.Read"**
8. Click **"Add permissions"** at the bottom
9. (Optional) If you're an admin, click **"Grant admin consent for..."**
   - If not, you'll be asked to consent when you first log in

### Step 7: Save Your Credentials

You should now have:
- ✅ **Application (client) ID**: `12345678-1234-1234-1234-123456789abc`
- ✅ **Client secret value**: A long random string

**Save both of these** - you'll add them to `.env` in Step 8.

### ✅ Microsoft Setup Complete!

---

## 🔷 Part 3: Slack OAuth Setup (10 minutes)

Slack will let you track @mentions in your workspace.

### Step 1: Go to Slack API

1. Open your browser and go to: **https://api.slack.com/apps**
2. Sign in to your Slack workspace
3. You should see "Your Apps" dashboard

### Step 2: Create a New App

1. Click **"Create New App"**
2. Choose **"From scratch"**
3. Fill in:
   - **App Name**: `Personal Dashboard`
   - **Pick a workspace**: Choose your workspace from the dropdown
4. Click **"Create App"**

### Step 3: Configure OAuth & Permissions

1. In the left sidebar, click **"OAuth & Permissions"**
2. Scroll down to **"Redirect URLs"**
3. Click **"Add New Redirect URL"**
4. Enter: `http://localhost:5000/auth/slack/callback`
5. Click **"Add"**
6. Click **"Save URLs"**

### Step 4: Add Scopes

Still on the "OAuth & Permissions" page:

1. Scroll down to **"Scopes"** section
2. Under **"User Token Scopes"** (NOT Bot Token Scopes), click **"Add an OAuth Scope"**
3. Add these scopes one by one:
   - ✅ `channels:history` - View messages in public channels
   - ✅ `channels:read` - View basic channel info
   - ✅ `groups:history` - View messages in private channels
   - ✅ `groups:read` - View basic private channel info
   - ✅ `im:history` - View messages in DMs
   - ✅ `mpim:history` - View messages in group DMs
   - ✅ `search:read` - Search messages
   - ✅ `users:read` - View people in workspace

### Step 5: Get Client ID and Secret

1. In the left sidebar, click **"Basic Information"**
2. Scroll to **"App Credentials"** section
3. Find **"Client ID"**:
   - It looks like: `1234567890.1234567890`
   - Click **"Show"** and copy it
   - **Save this** - you'll need it for `.env`
4. Find **"Client Secret"**:
   - Click **"Show"** to reveal it
   - Copy the secret
   - **Save this** - you'll need it for `.env`

### Step 6: Note About Installation

⚠️ **Important**: You don't install the app to your workspace yet. The dashboard will handle the OAuth flow when you first authenticate.

### ✅ Slack Setup Complete!

You should now have:
- ✅ **Slack Client ID**: `1234567890.1234567890`
- ✅ **Slack Client Secret**: A long random string

---

## 🔷 Part 4: Configure the .env File

Now let's put all your credentials together!

### Step 1: Copy the Example File

```bash
cd /home/user/Work-Tracker
cp .env.example .env
```

### Step 2: Edit the .env File

Open the `.env` file in your text editor:

```bash
nano .env
# or
vim .env
# or use any text editor
```

### Step 3: Fill in Your Credentials

Replace the placeholder values with your actual credentials:

```bash
# Flask Configuration
FLASK_SECRET_KEY=change-this-to-a-random-string-xyz123
PORT=5000

# Google OAuth (for Gmail, Calendar, Google Docs)
# These are automatically loaded from credentials/google_credentials.json
# Just make sure that file exists!

# Your Google Doc To-Do List ID
# Format: https://docs.google.com/document/d/YOUR_ID_HERE/edit
GOOGLE_DOC_ID=1dQSlBfc1Ptlqm31ZUuwT1KXKwe7LzR0qmO1sJSbOOeU

# Microsoft OAuth (for Outlook, Calendar)
MICROSOFT_CLIENT_ID=YOUR_MICROSOFT_CLIENT_ID_HERE
MICROSOFT_CLIENT_SECRET=YOUR_MICROSOFT_CLIENT_SECRET_HERE
MICROSOFT_TENANT_ID=common

# Slack OAuth
SLACK_CLIENT_ID=YOUR_SLACK_CLIENT_ID_HERE
SLACK_CLIENT_SECRET=YOUR_SLACK_CLIENT_SECRET_HERE

# Signal (Optional - requires signal-cli)
# SIGNAL_PHONE_NUMBER=+1234567890
# SIGNAL_CLI_PATH=signal-cli
```

### Step 4: Replace Placeholders

Go through and replace:

1. **FLASK_SECRET_KEY**: Generate a random string (keyboard mash is fine):
   ```
   FLASK_SECRET_KEY=asDf34JKL2kj3h4kj2h3k4jhSDFsdf234
   ```

2. **GOOGLE_DOC_ID**: Your Google Doc ID from Part 1, Step 7

3. **MICROSOFT_CLIENT_ID**: Your Application (client) ID from Part 2, Step 4

4. **MICROSOFT_CLIENT_SECRET**: Your Client Secret from Part 2, Step 5

5. **SLACK_CLIENT_ID**: Your Slack Client ID from Part 3, Step 5

6. **SLACK_CLIENT_SECRET**: Your Slack Client Secret from Part 3, Step 5

### Step 5: Save and Close

- In nano: Press `Ctrl+X`, then `Y`, then `Enter`
- In vim: Press `Esc`, type `:wq`, press `Enter`

### Step 6: Verify Your Files

Make sure you have:

```bash
ls -la credentials/
# Should show: google_credentials.json

cat .env | grep -v "^#" | grep -v "^$"
# Should show all your configuration without comments
```

### ✅ Configuration Complete!

---

## 🚀 Part 5: Run the Dashboard!

### Step 1: Install Dependencies

```bash
cd /home/user/Work-Tracker

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
python app.py
```

You should see:
```
Starting dashboard server on http://localhost:5000
 * Running on http://0.0.0.0:5000
```

### Step 3: Open in Browser

1. Open your web browser
2. Go to: **http://localhost:5000**
3. You should see your dashboard!

### Step 4: Authenticate Services

1. Click the **"🔐 Authenticate"** button in the top-right
2. You'll see the authentication status for each service
3. Click **"Connect Google"**:
   - You'll be redirected to Google
   - Sign in and grant permissions
   - You'll be redirected back to the dashboard
4. Click **"Connect Microsoft"**:
   - Same process with Microsoft
5. Click **"Connect Slack"**:
   - Same process with Slack

### Step 5: Watch the Magic! ✨

After authenticating:
- The dashboard will automatically fetch your data
- You'll see emails, calendar events, to-dos appear
- It refreshes every 5 minutes automatically
- Use the filter tabs to view specific types of items

---

## 🎉 You're All Set!

Your dashboard is now running and pulling data from:
- ✅ Gmail (flagged emails)
- ✅ Google Calendar
- ✅ Google Docs To-Do List
- ✅ Outlook (flagged emails)
- ✅ Outlook Calendar
- ✅ Slack (@mentions)

## 📌 Tips

### Keep it Running

To keep the dashboard running in the background:

**Option 1 - Use screen (Linux/Mac):**
```bash
screen -S dashboard
python app.py
# Press Ctrl+A, then D to detach
# Use "screen -r dashboard" to reattach
```

**Option 2 - Use tmux:**
```bash
tmux new -s dashboard
python app.py
# Press Ctrl+B, then D to detach
# Use "tmux attach -t dashboard" to reattach
```

### Autostart on Boot

Add to your crontab:
```bash
crontab -e
# Add this line:
@reboot cd /home/user/Work-Tracker && /home/user/Work-Tracker/venv/bin/python app.py
```

### Troubleshooting

**"Authentication failed"**
- Double-check your Client IDs and Secrets in `.env`
- Make sure redirect URIs are exactly `http://localhost:5000/auth/[service]/callback`
- Check that you enabled all required APIs (Google)
- Check that you added all required permissions (Microsoft, Slack)

**"No data showing"**
- Check browser console (F12) for errors
- Check Python console for errors
- Make sure you have flagged emails or upcoming calendar events
- Try the manual refresh button

**"Port already in use"**
- Change PORT in `.env` to a different number (e.g., 5001)
- Remember to update all redirect URIs!

---

## 🆘 Need Help?

If you run into issues:
1. Check the browser console (F12 → Console tab)
2. Check the Python console where app.py is running
3. Review this guide to make sure you didn't miss a step
4. Check that all your credentials are correct in `.env`
5. Verify `credentials/google_credentials.json` exists and is valid JSON

---

## 🎊 Congratulations!

You now have a personal productivity dashboard that aggregates everything important from your digital life into one place. Enjoy your new productivity superpower! 🚀
