"""
Slack Service
Handles Slack API authentication and data fetching for:
- Mentions and @-replies that are unresponded
"""

import os
import json
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

logger = logging.getLogger(__name__)

class SlackService:
    """Service for interacting with Slack API"""

    def __init__(self):
        self.token_file = 'tokens/slack_token.json'
        self.bot_token = None
        self.user_id = None
        self._load_token()

    def _load_token(self):
        """Load Slack token from file"""
        # First try to load from token file
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    token_data = json.load(f)
                    self.bot_token = token_data.get('access_token')
            except Exception as e:
                logger.error(f"Error loading Slack token: {e}")

        # Fallback to environment variable
        if not self.bot_token:
            self.bot_token = os.getenv('SLACK_BOT_TOKEN')

        # Get user ID if we have a token
        if self.bot_token:
            try:
                client = WebClient(token=self.bot_token)
                response = client.auth_test()
                self.user_id = response['user_id']
            except SlackApiError as e:
                logger.error(f"Error getting Slack user ID: {e}")

    def _save_token(self, token_data):
        """Save Slack token to file"""
        os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)
        self.bot_token = token_data.get('access_token')

    def is_authenticated(self):
        """Check if service is authenticated"""
        return self.bot_token is not None

    def get_auth_url(self):
        """Get OAuth authorization URL"""
        client_id = os.getenv('SLACK_CLIENT_ID')
        scopes = 'channels:history,channels:read,groups:history,groups:read,im:history,mpim:history,users:read,search:read'
        return f"https://slack.com/oauth/v2/authorize?client_id={client_id}&scope={scopes}&redirect_uri=http://localhost:5000/auth/slack/callback"

    def handle_auth_callback(self, code):
        """Handle OAuth callback"""
        import requests

        client_id = os.getenv('SLACK_CLIENT_ID')
        client_secret = os.getenv('SLACK_CLIENT_SECRET')

        response = requests.post('https://slack.com/api/oauth.v2.access', data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': 'http://localhost:5000/auth/slack/callback'
        })

        result = response.json()
        if result.get('ok'):
            token_data = {
                'access_token': result.get('access_token'),
                'team_id': result.get('team', {}).get('id')
            }
            self._save_token(token_data)
        else:
            logger.error(f"Error acquiring Slack token: {result.get('error')}")

    def get_unresponded_mentions(self):
        """
        Fetch mentions and @-replies that haven't been responded to
        """
        if not self.is_authenticated():
            return []

        client = WebClient(token=self.bot_token)
        mentions = []

        try:
            # Calculate timestamp for 7 days ago
            seven_days_ago = (datetime.now() - timedelta(days=7)).timestamp()

            # Search for messages that mention the user
            search_query = f"<@{self.user_id}>"
            response = client.search_messages(
                query=search_query,
                sort='timestamp',
                sort_dir='desc',
                count=50
            )

            if not response.get('ok'):
                return mentions

            for match in response.get('messages', {}).get('matches', []):
                message_ts = float(match.get('ts', 0))

                # Skip old messages
                if message_ts < seven_days_ago:
                    continue

                # Get the conversation to check if user replied
                channel = match.get('channel', {}).get('id')
                thread_ts = match.get('thread_ts', match.get('ts'))

                try:
                    # Get thread replies
                    replies_response = client.conversations_replies(
                        channel=channel,
                        ts=thread_ts,
                        limit=100
                    )

                    # Check if user has replied in this thread
                    user_replied = False
                    if replies_response.get('ok'):
                        for reply in replies_response.get('messages', []):
                            if reply.get('user') == self.user_id and reply.get('ts') != match.get('ts'):
                                user_replied = True
                                break

                    # If no reply, add to mentions list
                    if not user_replied:
                        channel_name = match.get('channel', {}).get('name', 'Unknown')
                        permalink = match.get('permalink', '')

                        mentions.append({
                            'text': match.get('text', ''),
                            'user': match.get('username', 'Unknown'),
                            'channel': channel_name,
                            'timestamp': datetime.fromtimestamp(message_ts).isoformat(),
                            'link': permalink,
                            'source': 'Slack'
                        })

                except SlackApiError as e:
                    logger.error(f"Error fetching Slack thread replies: {e}")
                    continue

        except SlackApiError as e:
            logger.error(f"Error searching Slack messages: {e}")

        return mentions
