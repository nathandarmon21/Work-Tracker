# Personal Dashboard

A comprehensive personal productivity dashboard that aggregates tasks, emails, mentions, and events from multiple sources into a single, easy-to-use interface.

## Features

### Work To-Dos
- **Gmail**: Flagged/important emails (filtered for spam)
- **Outlook**: Flagged/important emails
- **Slack**: Unresponded @mentions
- **Signal**: Recent mentions (requires signal-cli)
- **Google Docs**: Unchecked to-do items from your shared document

### Events & Calendar
- **Google Calendar**: Upcoming events (next 7 days)
- **Outlook Calendar**: Upcoming events
- **Harvard Law Events**: Curated events from weekly emails
- **Weekly Events in Boston**: Custom event tracking

### Dashboard Features
- Auto-refresh every 5 minutes
- Priority-based sorting
- Filter by type (emails, mentions, tasks)
- Clean, modern interface
- Real-time statistics

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Web browser

### Step 1: Clone and Setup

```bash
# Clone the repository (if needed)
cd /home/user/Work-Tracker

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials (see OAuth Setup below)
nano .env  # or use your preferred editor
```

### Step 3: Set Up OAuth Credentials

You need to create OAuth applications for each service. Follow the detailed guides below.

## OAuth Setup Guide

### Google (Gmail, Calendar, Google Docs)

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Create a new project or select an existing one

2. **Enable APIs**
   - Go to "APIs & Services" > "Library"
   - Enable the following APIs:
     - Gmail API
     - Google Calendar API
     - Google Docs API

3. **Create OAuth Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: "Web application"
   - Name: "Personal Dashboard"
   - Authorized redirect URIs: `http://localhost:5000/auth/google/callback`
   - Click "Create"

4. **Download Credentials**
   - Click the download button (⬇) next to your OAuth client
   - Save the file as `credentials/google_credentials.json`

5. **Update .env**
   - Open the downloaded JSON file
   - Copy `client_id` to `GOOGLE_CLIENT_ID` in .env
   - Copy `client_secret` to `GOOGLE_CLIENT_SECRET` in .env

### Microsoft (Outlook, Calendar)

1. **Go to Azure Portal**
   - Visit: https://portal.azure.com/
   - Go to "Azure Active Directory" > "App registrations"

2. **Register Application**
   - Click "New registration"
   - Name: "Personal Dashboard"
   - Supported account types: "Accounts in any organizational directory and personal Microsoft accounts"
   - Redirect URI: Web - `http://localhost:5000/auth/microsoft/callback`
   - Click "Register"

3. **Configure API Permissions**
   - Go to "API permissions"
   - Click "Add a permission" > "Microsoft Graph"
   - Select "Delegated permissions"
   - Add these permissions:
     - Mail.Read
     - Calendars.Read
   - Click "Add permissions"
   - Click "Grant admin consent" (if you're an admin)

4. **Create Client Secret**
   - Go to "Certificates & secrets"
   - Click "New client secret"
   - Description: "Dashboard Secret"
   - Expires: Choose your preference (12 months recommended)
   - Click "Add"
   - **Copy the secret VALUE immediately** (you won't see it again!)

5. **Update .env**
   - Copy "Application (client) ID" to `MICROSOFT_CLIENT_ID`
   - Copy the client secret value to `MICROSOFT_CLIENT_SECRET`

### Slack

1. **Create Slack App**
   - Visit: https://api.slack.com/apps
   - Click "Create New App" > "From scratch"
   - App Name: "Personal Dashboard"
   - Choose your workspace

2. **Configure OAuth & Permissions**
   - Go to "OAuth & Permissions"
   - Under "Redirect URLs", add: `http://localhost:5000/auth/slack/callback`
   - Under "Scopes" > "User Token Scopes", add:
     - channels:history
     - channels:read
     - groups:history
     - groups:read
     - im:history
     - mpim:history
     - users:read
     - search:read

3. **Get Credentials**
   - Go to "Basic Information"
   - Copy "Client ID" to `SLACK_CLIENT_ID` in .env
   - Copy "Client Secret" to `SLACK_CLIENT_SECRET` in .env

4. **Install to Workspace**
   - You'll complete this step when you first run the app

### Signal (Optional)

Signal requires signal-cli to be installed. This is optional and more complex to set up.

1. **Install signal-cli**
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install signal-cli

   # On macOS
   brew install signal-cli

   # Or download from: https://github.com/AsamK/signal-cli
   ```

2. **Register Phone Number**
   ```bash
   signal-cli -a +YOUR_PHONE_NUMBER register
   signal-cli -a +YOUR_PHONE_NUMBER verify VERIFICATION_CODE
   ```

3. **Update .env**
   ```
   SIGNAL_PHONE_NUMBER=+YOUR_PHONE_NUMBER
   SIGNAL_CLI_PATH=signal-cli  # or full path if needed
   ```

## Running the Dashboard

### Step 1: Create Required Directories

```bash
mkdir -p credentials tokens
```

### Step 2: Start the Server

```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the application
python app.py
```

You should see:
```
Starting dashboard server on http://localhost:5000
 * Running on http://0.0.0.0:5000
```

### Step 3: Access the Dashboard

1. Open your web browser
2. Go to: http://localhost:5000
3. Click the "🔐 Authenticate" button
4. Connect each service (Google, Microsoft, Slack)
5. The dashboard will automatically start fetching your data!

## Usage

### First Time Setup

1. After starting the server, click "🔐 Authenticate"
2. Connect each service by clicking the respective "Connect" buttons
3. You'll be redirected to each service to authorize the app
4. After authorization, you'll be redirected back to the dashboard
5. The dashboard will automatically fetch and display your data

### Daily Use

1. Open http://localhost:5000 in your browser
2. The dashboard auto-refreshes every 5 minutes
3. Use the filter tabs to view specific types of items
4. Click "↻ Refresh" for manual updates
5. Click on any item to view it in the original application

## Customization

### Change Refresh Interval

Edit `app.py`:
```python
# Change minutes=5 to your preferred interval
scheduler.add_job(fetch_dashboard_data, 'interval', minutes=5)
```

### Modify Filters

Edit `services/aggregator.py` to customize spam filtering, priority assignment, or data processing logic.

### Customize Appearance

Edit `static/css/style.css` to change colors, layout, or styling.

## Troubleshooting

### "Authentication failed" errors

1. Double-check your credentials in .env
2. Ensure redirect URIs match exactly: `http://localhost:5000/auth/[service]/callback`
3. Make sure all required API permissions are granted
4. Clear tokens folder: `rm -rf tokens/*` and re-authenticate

### No data showing up

1. Check the browser console (F12) for errors
2. Check the Python console for error messages
3. Verify you've granted all required permissions
4. Try the manual refresh button
5. Check if your email/calendar has actual flagged items

### Signal not working

Signal integration is optional and requires signal-cli installation. If you don't need Signal:
1. Just skip the Signal setup
2. The dashboard will work fine without it

### Port already in use

If port 5000 is already in use, change it in .env:
```
PORT=5001
```

And update all OAuth redirect URIs to use the new port.

## Security Notes

- All credentials are stored locally in the `tokens/` directory
- Never commit `.env` or `tokens/` to version control
- OAuth tokens are encrypted by the respective services
- The dashboard only has read-only access to your data
- Consider setting up firewall rules if exposing to network

## Project Structure

```
Work-Tracker/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── .env.example           # Example environment variables
├── README.md              # This file
├── services/              # Data fetching services
│   ├── gmail_service.py   # Gmail, Calendar, Docs integration
│   ├── outlook_service.py # Outlook, Calendar integration
│   ├── slack_service.py   # Slack integration
│   ├── signal_service.py  # Signal integration (optional)
│   └── aggregator.py      # Data aggregation logic
├── templates/             # HTML templates
│   └── dashboard.html     # Main dashboard page
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Dashboard styling
│   └── js/
│       └── dashboard.js   # Dashboard JavaScript
├── credentials/           # OAuth credentials (create this)
│   └── google_credentials.json
└── tokens/               # OAuth tokens (auto-created)
    ├── google_token.pickle
    ├── microsoft_token.json
    └── slack_token.json
```

## Future Enhancements

Potential features to add:
- Task completion tracking
- Email response drafting
- Calendar event creation
- Notification system
- Mobile-responsive design improvements
- Dark mode
- Multiple user support
- Export to CSV/PDF
- Integration with more services (Notion, Todoist, etc.)

## License

This project is for personal use. Modify as needed for your workflow.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the console logs for specific error messages
3. Ensure all OAuth credentials are correctly configured
4. Verify all required APIs are enabled in respective consoles

## Credits

Built with:
- Flask (Python web framework)
- Google APIs
- Microsoft Graph API
- Slack API
- signal-cli
