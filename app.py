"""
Personal Dashboard Application
Main Flask application that serves the dashboard and API endpoints
"""

import os
import json
from flask import Flask, render_template, jsonify, redirect, url_for, session, request
from flask_cors import CORS
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# Import our data fetchers
from services.gmail_service import GmailService
from services.outlook_service import OutlookService
from services.slack_service import SlackService
from services.signal_service import SignalService
from services.aggregator import DashboardAggregator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# Initialize services
gmail_service = GmailService()
outlook_service = OutlookService()
slack_service = SlackService()
signal_service = SignalService()
aggregator = DashboardAggregator(gmail_service, outlook_service, slack_service, signal_service)

# Global variable to store dashboard data
dashboard_data = {
    'work_todos': [],
    'events': [],
    'last_updated': None,
    'errors': []
}

def fetch_dashboard_data():
    """Background task to fetch all dashboard data"""
    global dashboard_data
    try:
        logger.info("Fetching dashboard data...")
        dashboard_data = aggregator.fetch_all_data()
        logger.info(f"Dashboard data updated at {dashboard_data['last_updated']}")
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {e}")
        dashboard_data['errors'].append(str(e))

# Set up background scheduler for auto-refresh (every 5 minutes)
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_dashboard_data, 'interval', minutes=5)
scheduler.start()

# Routes
@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/dashboard')
def get_dashboard_data():
    """API endpoint to get current dashboard data"""
    return jsonify(dashboard_data)

@app.route('/api/refresh')
def refresh_data():
    """Manual refresh endpoint"""
    fetch_dashboard_data()
    return jsonify({'status': 'success', 'message': 'Data refreshed'})

# OAuth callback routes
@app.route('/auth/google')
def auth_google():
    """Initiate Google OAuth flow"""
    return gmail_service.get_auth_url()

@app.route('/auth/google/callback')
def auth_google_callback():
    """Handle Google OAuth callback"""
    code = request.args.get('code')
    if code:
        gmail_service.handle_auth_callback(code)
        return redirect('/')
    return "Authentication failed", 400

@app.route('/auth/microsoft')
def auth_microsoft():
    """Initiate Microsoft OAuth flow"""
    return outlook_service.get_auth_url()

@app.route('/auth/microsoft/callback')
def auth_microsoft_callback():
    """Handle Microsoft OAuth callback"""
    code = request.args.get('code')
    if code:
        outlook_service.handle_auth_callback(code)
        return redirect('/')
    return "Authentication failed", 400

@app.route('/auth/slack')
def auth_slack():
    """Initiate Slack OAuth flow"""
    return slack_service.get_auth_url()

@app.route('/auth/slack/callback')
def auth_slack_callback():
    """Handle Slack OAuth callback"""
    code = request.args.get('code')
    if code:
        slack_service.handle_auth_callback(code)
        return redirect('/')
    return "Authentication failed", 400

@app.route('/api/auth/status')
def auth_status():
    """Check authentication status for all services"""
    return jsonify({
        'google': gmail_service.is_authenticated(),
        'microsoft': outlook_service.is_authenticated(),
        'slack': slack_service.is_authenticated(),
        'signal': signal_service.is_authenticated()
    })

if __name__ == '__main__':
    # Fetch initial data
    fetch_dashboard_data()

    # Run the Flask app
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting dashboard server on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
