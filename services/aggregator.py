"""
Dashboard Aggregator
Combines data from all services and organizes it for the dashboard
"""

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DashboardAggregator:
    """Aggregates data from all services for the dashboard"""

    def __init__(self, gmail_service, outlook_service, slack_service, signal_service):
        self.gmail_service = gmail_service
        self.outlook_service = outlook_service
        self.slack_service = slack_service
        self.signal_service = signal_service

    def fetch_all_data(self):
        """
        Fetch data from all sources and organize it
        Returns a dictionary with work_todos and events
        """
        work_todos = []
        events = []
        errors = []

        # 1. Fetch flagged emails from Gmail
        try:
            logger.info("Fetching Gmail emails...")
            gmail_emails = self.gmail_service.get_flagged_emails()
            for email in gmail_emails:
                work_todos.append({
                    'type': 'email',
                    'title': f"Email: {email['subject']}",
                    'description': f"From: {email['from']}",
                    'snippet': email['snippet'],
                    'link': email['link'],
                    'source': email['source'],
                    'date': email['date'],
                    'priority': 'high' if 'important' in email.get('snippet', '').lower() else 'medium'
                })
        except Exception as e:
            logger.error(f"Error fetching Gmail emails: {e}")
            errors.append(f"Gmail emails: {str(e)}")

        # 2. Fetch flagged emails from Outlook
        try:
            logger.info("Fetching Outlook emails...")
            outlook_emails = self.outlook_service.get_flagged_emails()
            for email in outlook_emails:
                work_todos.append({
                    'type': 'email',
                    'title': f"Email: {email['subject']}",
                    'description': f"From: {email['from']}",
                    'snippet': email['snippet'],
                    'link': email['link'],
                    'source': email['source'],
                    'date': email['date'],
                    'priority': 'high'
                })
        except Exception as e:
            logger.error(f"Error fetching Outlook emails: {e}")
            errors.append(f"Outlook emails: {str(e)}")

        # 3. Fetch Slack mentions
        try:
            logger.info("Fetching Slack mentions...")
            slack_mentions = self.slack_service.get_unresponded_mentions()
            for mention in slack_mentions:
                work_todos.append({
                    'type': 'mention',
                    'title': f"Slack mention in #{mention['channel']}",
                    'description': f"From {mention['user']}: {mention['text'][:100]}...",
                    'snippet': mention['text'],
                    'link': mention['link'],
                    'source': mention['source'],
                    'date': mention['timestamp'],
                    'priority': 'high'
                })
        except Exception as e:
            logger.error(f"Error fetching Slack mentions: {e}")
            errors.append(f"Slack mentions: {str(e)}")

        # 4. Fetch Signal mentions
        try:
            logger.info("Fetching Signal mentions...")
            signal_mentions = self.signal_service.get_unresponded_mentions()
            for mention in signal_mentions:
                work_todos.append({
                    'type': 'mention',
                    'title': f"Signal message from {mention['from']}",
                    'description': mention['text'][:100],
                    'snippet': mention['text'],
                    'link': '#',  # Signal doesn't have web links
                    'source': mention['source'],
                    'date': mention['timestamp'],
                    'priority': 'medium'
                })
        except Exception as e:
            logger.error(f"Error fetching Signal mentions: {e}")
            errors.append(f"Signal mentions: {str(e)}")

        # 5. Fetch Google Calendar events
        try:
            logger.info("Fetching Google Calendar events...")
            google_events = self.gmail_service.get_calendar_events()
            for event in google_events:
                events.append({
                    'type': 'calendar',
                    'title': event['summary'],
                    'description': event.get('description', ''),
                    'location': event.get('location', ''),
                    'start': event['start'],
                    'end': event['end'],
                    'link': event['link'],
                    'source': event['source']
                })
        except Exception as e:
            logger.error(f"Error fetching Google Calendar events: {e}")
            errors.append(f"Google Calendar: {str(e)}")

        # 6. Fetch Outlook Calendar events
        try:
            logger.info("Fetching Outlook Calendar events...")
            outlook_events = self.outlook_service.get_calendar_events()
            for event in outlook_events:
                events.append({
                    'type': 'calendar',
                    'title': event['summary'],
                    'description': event.get('description', ''),
                    'location': event.get('location', ''),
                    'start': event['start'],
                    'end': event['end'],
                    'link': event['link'],
                    'source': event['source']
                })
        except Exception as e:
            logger.error(f"Error fetching Outlook Calendar events: {e}")
            errors.append(f"Outlook Calendar: {str(e)}")

        # 7. Fetch Google Doc to-dos
        try:
            logger.info("Fetching Google Doc to-dos...")
            doc_todos = self.gmail_service.get_google_doc_todos()
            for todo in doc_todos:
                work_todos.append({
                    'type': 'todo',
                    'title': todo['text'],
                    'description': 'From your Google Doc to-do list',
                    'snippet': '',
                    'link': todo['link'],
                    'source': todo['source'],
                    'date': datetime.now().isoformat(),
                    'priority': 'medium'
                })
        except Exception as e:
            logger.error(f"Error fetching Google Doc todos: {e}")
            errors.append(f"Google Doc todos: {str(e)}")

        # 8. Fetch Harvard Law events
        try:
            logger.info("Fetching Harvard Law events...")
            harvard_events = self.outlook_service.get_harvard_law_events()
            for event in harvard_events:
                events.append({
                    'type': 'event',
                    'title': event['title'],
                    'description': event['description'],
                    'start': event['date'],
                    'link': event['link'],
                    'source': event['source'],
                    'preview': event.get('raw_content', '')
                })
        except Exception as e:
            logger.error(f"Error fetching Harvard Law events: {e}")
            errors.append(f"Harvard Law events: {str(e)}")

        # Sort work todos by priority and date
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        work_todos.sort(key=lambda x: (priority_order.get(x.get('priority', 'low'), 2), x.get('date', '')), reverse=True)

        # Sort events by start date
        events.sort(key=lambda x: x.get('start', ''))

        return {
            'work_todos': work_todos,
            'events': events,
            'last_updated': datetime.now().isoformat(),
            'errors': errors,
            'stats': {
                'total_todos': len(work_todos),
                'total_events': len(events),
                'high_priority': len([t for t in work_todos if t.get('priority') == 'high']),
                'emails': len([t for t in work_todos if t.get('type') == 'email']),
                'mentions': len([t for t in work_todos if t.get('type') == 'mention']),
                'todos': len([t for t in work_todos if t.get('type') == 'todo'])
            }
        }
