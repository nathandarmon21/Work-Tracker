"""
Gmail Service
Handles Gmail API authentication and data fetching for:
- Flagged/important emails
- Google Calendar events
- Google Docs to-do list
"""

import os
import json
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

logger = logging.getLogger(__name__)

class GmailService:
    """Service for interacting with Gmail, Calendar, and Google Docs APIs"""

    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/calendar.readonly',
        'https://www.googleapis.com/auth/documents.readonly'
    ]

    def __init__(self):
        self.creds = None
        self.token_file = 'tokens/google_token.pickle'
        self.credentials_file = 'credentials/google_credentials.json'
        self._load_credentials()

    def _load_credentials(self):
        """Load credentials from token file"""
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)

        # Refresh if expired
        if self.creds and self.creds.expired and self.creds.refresh_token:
            try:
                self.creds.refresh(Request())
                self._save_credentials()
            except Exception as e:
                logger.error(f"Error refreshing Google credentials: {e}")
                self.creds = None

    def _save_credentials(self):
        """Save credentials to token file"""
        os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
        with open(self.token_file, 'wb') as token:
            pickle.dump(self.creds, token)

    def is_authenticated(self):
        """Check if service is authenticated"""
        return self.creds is not None and self.creds.valid

    def get_auth_url(self):
        """Get OAuth authorization URL"""
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=self.SCOPES,
            redirect_uri='http://localhost:5000/auth/google/callback'
        )
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        return auth_url

    def handle_auth_callback(self, code):
        """Handle OAuth callback"""
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=self.SCOPES,
            redirect_uri='http://localhost:5000/auth/google/callback'
        )
        flow.fetch_token(code=code)
        self.creds = flow.credentials
        self._save_credentials()

    def get_flagged_emails(self):
        """Fetch flagged/important emails from Gmail"""
        if not self.is_authenticated():
            return []

        try:
            service = build('gmail', 'v1', credentials=self.creds)

            # Search for starred/important emails from the last 7 days
            query = 'is:starred OR is:important newer_than:7d'
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=20
            ).execute()

            messages = results.get('messages', [])
            emails = []

            for msg in messages:
                try:
                    message = service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='metadata',
                        metadataHeaders=['From', 'Subject', 'Date']
                    ).execute()

                    headers = {h['name']: h['value'] for h in message['payload']['headers']}

                    # Filter out spam and promotional emails
                    subject = headers.get('Subject', '')
                    from_email = headers.get('From', '')

                    # Basic spam filtering
                    spam_keywords = ['unsubscribe', 'promotional', 'newsletter', 'marketing']
                    if any(keyword in subject.lower() or keyword in from_email.lower()
                           for keyword in spam_keywords):
                        continue

                    emails.append({
                        'id': msg['id'],
                        'subject': subject,
                        'from': from_email,
                        'date': headers.get('Date', ''),
                        'snippet': message.get('snippet', ''),
                        'link': f"https://mail.google.com/mail/u/0/#inbox/{msg['id']}",
                        'source': 'Gmail'
                    })
                except HttpError as e:
                    logger.error(f"Error fetching Gmail message {msg['id']}: {e}")
                    continue

            return emails

        except HttpError as e:
            logger.error(f"Error fetching Gmail emails: {e}")
            return []

    def get_calendar_events(self):
        """Fetch important calendar events from Google Calendar"""
        if not self.is_authenticated():
            return []

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # Get events for the next 7 days
            now = datetime.utcnow()
            time_min = now.isoformat() + 'Z'
            time_max = (now + timedelta(days=7)).isoformat() + 'Z'

            events_result = service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                maxResults=20,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])
            calendar_events = []

            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                calendar_events.append({
                    'id': event['id'],
                    'summary': event.get('summary', 'No Title'),
                    'start': start,
                    'end': event['end'].get('dateTime', event['end'].get('date')),
                    'location': event.get('location', ''),
                    'description': event.get('description', ''),
                    'link': event.get('htmlLink', ''),
                    'source': 'Google Calendar'
                })

            return calendar_events

        except HttpError as e:
            logger.error(f"Error fetching Google Calendar events: {e}")
            return []

    def get_google_doc_todos(self):
        """Fetch unchecked items from Google Doc to-do list"""
        if not self.is_authenticated():
            return []

        try:
            doc_id = os.getenv('GOOGLE_DOC_ID')
            if not doc_id:
                logger.warning("GOOGLE_DOC_ID not set in environment")
                return []

            service = build('docs', 'v1', credentials=self.creds)
            document = service.documents().get(documentId=doc_id).execute()

            todos = []
            content = document.get('body', {}).get('content', [])

            for element in content:
                if 'paragraph' in element:
                    paragraph = element['paragraph']
                    # Check for bullet lists
                    if 'bullet' in paragraph:
                        text_elements = paragraph.get('elements', [])
                        for text_element in text_elements:
                            if 'textRun' in text_element:
                                text = text_element['textRun'].get('content', '').strip()
                                # Look for unchecked boxes (☐) or tasks without checkmarks
                                if text and ('☐' in text or ('☑' not in text and '✓' not in text and len(text) > 2)):
                                    # Clean up the text
                                    clean_text = text.replace('☐', '').replace('☑', '').replace('✓', '').strip()
                                    if clean_text:
                                        todos.append({
                                            'text': clean_text,
                                            'source': 'Google Doc To-Do',
                                            'link': f"https://docs.google.com/document/d/{doc_id}/edit"
                                        })

            return todos

        except HttpError as e:
            logger.error(f"Error fetching Google Doc todos: {e}")
            return []
