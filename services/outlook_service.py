"""
Outlook Service
Handles Microsoft Graph API authentication and data fetching for:
- Flagged/important emails from Outlook
- Outlook Calendar events
"""

import os
import json
import requests
from datetime import datetime, timedelta
import msal
import logging

logger = logging.getLogger(__name__)

class OutlookService:
    """Service for interacting with Microsoft Graph API (Outlook)"""

    SCOPES = [
        'https://graph.microsoft.com/Mail.Read',
        'https://graph.microsoft.com/Calendars.Read'
    ]

    def __init__(self):
        self.client_id = os.getenv('MICROSOFT_CLIENT_ID')
        self.client_secret = os.getenv('MICROSOFT_CLIENT_SECRET')
        self.tenant_id = os.getenv('MICROSOFT_TENANT_ID', 'common')
        self.token_file = 'tokens/microsoft_token.json'
        self.access_token = None
        self._load_token()

    def _load_token(self):
        """Load access token from file"""
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    token_data = json.load(f)
                    self.access_token = token_data.get('access_token')
            except Exception as e:
                logger.error(f"Error loading Microsoft token: {e}")

    def _save_token(self, token_data):
        """Save access token to file"""
        os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)
        self.access_token = token_data.get('access_token')

    def is_authenticated(self):
        """Check if service is authenticated"""
        return self.access_token is not None

    def get_auth_url(self):
        """Get OAuth authorization URL"""
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            client_credential=self.client_secret
        )

        auth_url = app.get_authorization_request_url(
            scopes=self.SCOPES,
            redirect_uri='http://localhost:5000/auth/microsoft/callback'
        )
        return auth_url

    def handle_auth_callback(self, code):
        """Handle OAuth callback"""
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            client_credential=self.client_secret
        )

        result = app.acquire_token_by_authorization_code(
            code,
            scopes=self.SCOPES,
            redirect_uri='http://localhost:5000/auth/microsoft/callback'
        )

        if "access_token" in result:
            self._save_token(result)
        else:
            logger.error(f"Error acquiring Microsoft token: {result.get('error_description')}")

    def _make_graph_request(self, endpoint):
        """Make a request to Microsoft Graph API"""
        if not self.access_token:
            return None

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(
                f'https://graph.microsoft.com/v1.0{endpoint}',
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making Graph API request: {e}")
            return None

    def get_flagged_emails(self):
        """Fetch flagged/important emails from Outlook"""
        if not self.is_authenticated():
            return []

        # Get flagged emails from the last 7 days
        filter_query = "flag/flagStatus eq 'flagged' or importance eq 'high'"
        endpoint = f"/me/messages?$filter={filter_query}&$top=20&$orderby=receivedDateTime desc"

        result = self._make_graph_request(endpoint)
        if not result:
            return []

        emails = []
        for msg in result.get('value', []):
            subject = msg.get('subject', '')
            from_email = msg.get('from', {}).get('emailAddress', {}).get('address', '')

            # Basic spam filtering
            spam_keywords = ['unsubscribe', 'promotional', 'newsletter', 'marketing']
            if any(keyword in subject.lower() or keyword in from_email.lower()
                   for keyword in spam_keywords):
                continue

            emails.append({
                'id': msg['id'],
                'subject': subject,
                'from': msg.get('from', {}).get('emailAddress', {}).get('name', from_email),
                'date': msg.get('receivedDateTime', ''),
                'snippet': msg.get('bodyPreview', ''),
                'link': msg.get('webLink', ''),
                'source': 'Outlook'
            })

        return emails

    def get_calendar_events(self):
        """Fetch important calendar events from Outlook Calendar"""
        if not self.is_authenticated():
            return []

        # Get events for the next 7 days
        now = datetime.utcnow()
        time_min = now.isoformat() + 'Z'
        time_max = (now + timedelta(days=7)).isoformat() + 'Z'

        endpoint = f"/me/calendar/events?$filter=start/dateTime ge '{time_min}' and start/dateTime le '{time_max}'&$top=20&$orderby=start/dateTime"

        result = self._make_graph_request(endpoint)
        if not result:
            return []

        events = []
        for event in result.get('value', []):
            events.append({
                'id': event['id'],
                'summary': event.get('subject', 'No Title'),
                'start': event['start']['dateTime'],
                'end': event['end']['dateTime'],
                'location': event.get('location', {}).get('displayName', ''),
                'description': event.get('bodyPreview', ''),
                'link': event.get('webLink', ''),
                'source': 'Outlook Calendar'
            })

        return events

    def get_harvard_law_events(self):
        """
        Parse emails from news@law.harvard.edu for weekly events
        This looks for the "Events at Harvard Law" email
        """
        if not self.is_authenticated():
            return []

        # Search for emails from Harvard Law News
        endpoint = "/me/messages?$filter=from/emailAddress/address eq 'news@law.harvard.edu'&$top=5&$orderby=receivedDateTime desc"

        result = self._make_graph_request(endpoint)
        if not result:
            return []

        events = []
        for msg in result.get('value', []):
            subject = msg.get('subject', '')

            # Look for "Events at Harvard Law" emails
            if 'events' in subject.lower() and 'harvard law' in subject.lower():
                # Get full email body
                body_endpoint = f"/me/messages/{msg['id']}"
                full_msg = self._make_graph_request(body_endpoint)

                if full_msg:
                    body_content = full_msg.get('body', {}).get('content', '')

                    # Simple parsing - this could be enhanced based on email format
                    # For now, we'll return the email link for manual review
                    events.append({
                        'title': subject,
                        'description': 'Harvard Law Events - Click to view details',
                        'date': msg.get('receivedDateTime', ''),
                        'link': msg.get('webLink', ''),
                        'source': 'Harvard Law Events',
                        'raw_content': body_content[:500]  # First 500 chars as preview
                    })

        return events
