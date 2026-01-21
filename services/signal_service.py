"""
Signal Service
Handles Signal message fetching for mentions

NOTE: Signal does not have an official API. This service requires signal-cli
to be installed and configured. See setup documentation for details.
"""

import os
import json
import subprocess
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SignalService:
    """
    Service for interacting with Signal messages via signal-cli

    This requires signal-cli to be installed and configured.
    See: https://github.com/AsamK/signal-cli
    """

    def __init__(self):
        self.phone_number = os.getenv('SIGNAL_PHONE_NUMBER')
        self.signal_cli_path = os.getenv('SIGNAL_CLI_PATH', 'signal-cli')

    def is_authenticated(self):
        """
        Check if signal-cli is installed and configured
        """
        try:
            result = subprocess.run(
                [self.signal_cli_path, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def get_unresponded_mentions(self):
        """
        Fetch Signal messages with mentions

        This is a basic implementation that requires signal-cli.
        Due to Signal's architecture, this is limited and may not work
        perfectly for all use cases.
        """
        if not self.is_authenticated():
            logger.info("Signal integration not configured (signal-cli not found)")
            return []

        if not self.phone_number:
            logger.warning("SIGNAL_PHONE_NUMBER not set in environment")
            return []

        try:
            # Receive messages using signal-cli
            result = subprocess.run(
                [self.signal_cli_path, '-a', self.phone_number, 'receive', '--json'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                logger.error(f"Error receiving Signal messages: {result.stderr}")
                return []

            mentions = []
            seven_days_ago = datetime.now() - timedelta(days=7)

            # Parse JSON output
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue

                try:
                    message = json.loads(line)
                    envelope = message.get('envelope', {})
                    data_message = envelope.get('dataMessage', {})

                    # Check if message has mentions (this is simplified)
                    message_text = data_message.get('message', '')
                    timestamp = envelope.get('timestamp', 0) / 1000  # Convert to seconds

                    # Skip old messages
                    message_time = datetime.fromtimestamp(timestamp)
                    if message_time < seven_days_ago:
                        continue

                    # Check for @mentions or if message is in a group
                    if '@' in message_text or data_message.get('groupInfo'):
                        mentions.append({
                            'text': message_text,
                            'from': envelope.get('source', 'Unknown'),
                            'timestamp': message_time.isoformat(),
                            'group': data_message.get('groupInfo', {}).get('groupId', ''),
                            'source': 'Signal'
                        })

                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing Signal message JSON: {e}")
                    continue

            return mentions

        except subprocess.TimeoutExpired:
            logger.error("Timeout receiving Signal messages")
            return []
        except Exception as e:
            logger.error(f"Error fetching Signal messages: {e}")
            return []
