#!/usr/bin/env python3
"""
Interactive Setup Script for Personal Dashboard
Guides users through the setup process
"""

import os
import sys
import json
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def print_step(number, text):
    """Print a step number"""
    print(f"\n{'─' * 60}")
    print(f"STEP {number}: {text}")
    print('─' * 60)

def check_python_version():
    """Ensure Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   You have Python {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def create_directories():
    """Create required directories"""
    dirs = ['credentials', 'tokens', 'services', 'templates', 'static/css', 'static/js']
    for dir_name in dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
    print("✅ Created required directories")

def setup_env_file():
    """Set up .env file"""
    if os.path.exists('.env'):
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("   Keeping existing .env file")
            return

    if not os.path.exists('.env.example'):
        print("❌ Error: .env.example not found")
        return

    # Copy .env.example to .env
    with open('.env.example', 'r') as f:
        content = f.read()

    with open('.env', 'w') as f:
        f.write(content)

    print("✅ Created .env file from template")
    print("   You'll need to edit this file with your credentials")

def check_google_credentials():
    """Check if Google credentials exist"""
    cred_file = 'credentials/google_credentials.json'
    if os.path.exists(cred_file):
        print(f"✅ Found {cred_file}")
        return True
    else:
        print(f"❌ {cred_file} not found")
        print("\n   How to get Google credentials:")
        print("   1. Go to https://console.cloud.google.com/")
        print("   2. Create a new project")
        print("   3. Enable Gmail API, Calendar API, and Docs API")
        print("   4. Create OAuth 2.0 credentials (Web application)")
        print("   5. Add redirect URI: http://localhost:5000/auth/google/callback")
        print("   6. Download credentials JSON")
        print(f"   7. Save as: {cred_file}")
        return False

def configure_env():
    """Interactive configuration of .env file"""
    print("\n📝 Let's configure your services...")

    if not os.path.exists('.env'):
        print("❌ Error: .env file not found. Run setup first.")
        return

    print("\nYou'll need to set up OAuth applications for each service.")
    print("See README.md for detailed instructions.\n")

    # Microsoft
    print("Microsoft (Outlook):")
    ms_client_id = input("  Enter Microsoft Client ID (or press Enter to skip): ").strip()
    if ms_client_id:
        ms_client_secret = input("  Enter Microsoft Client Secret: ").strip()
        update_env('MICROSOFT_CLIENT_ID', ms_client_id)
        update_env('MICROSOFT_CLIENT_SECRET', ms_client_secret)
        print("  ✅ Microsoft configured")
    else:
        print("  ⏭️  Skipped Microsoft setup")

    # Slack
    print("\nSlack:")
    slack_client_id = input("  Enter Slack Client ID (or press Enter to skip): ").strip()
    if slack_client_id:
        slack_client_secret = input("  Enter Slack Client Secret: ").strip()
        update_env('SLACK_CLIENT_ID', slack_client_id)
        update_env('SLACK_CLIENT_SECRET', slack_client_secret)
        print("  ✅ Slack configured")
    else:
        print("  ⏭️  Skipped Slack setup")

    # Google Doc ID
    print("\nGoogle Doc To-Do List:")
    print("  Your doc URL looks like:")
    print("  https://docs.google.com/document/d/YOUR_DOC_ID/edit")
    doc_id = input("  Enter your Google Doc ID (or press Enter to skip): ").strip()
    if doc_id:
        update_env('GOOGLE_DOC_ID', doc_id)
        print("  ✅ Google Doc configured")
    else:
        print("  ⏭️  Skipped Google Doc setup")

    print("\n✅ Configuration complete!")

def update_env(key, value):
    """Update a value in .env file"""
    with open('.env', 'r') as f:
        lines = f.readlines()

    with open('.env', 'w') as f:
        found = False
        for line in lines:
            if line.startswith(f'{key}='):
                f.write(f'{key}={value}\n')
                found = True
            else:
                f.write(line)

        if not found:
            f.write(f'{key}={value}\n')

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    print("   This may take a few minutes...\n")

    import subprocess
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("\n✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Error installing dependencies")
        print("   Try running manually: pip install -r requirements.txt")
        return False

def main():
    """Main setup flow"""
    print_header("Personal Dashboard Setup")

    print("This script will guide you through setting up your dashboard.\n")

    # Step 1: Check Python version
    print_step(1, "Checking Python Version")
    check_python_version()

    # Step 2: Create directories
    print_step(2, "Creating Directories")
    create_directories()

    # Step 3: Set up .env file
    print_step(3, "Setting up Environment File")
    setup_env_file()

    # Step 4: Check Google credentials
    print_step(4, "Checking Google Credentials")
    has_google = check_google_credentials()

    # Step 5: Install dependencies
    print_step(5, "Installing Dependencies")
    install = input("\nInstall Python dependencies now? (Y/n): ").lower()
    if install != 'n':
        install_dependencies()
    else:
        print("⏭️  Skipped dependency installation")
        print("   Run later with: pip install -r requirements.txt")

    # Step 6: Configure services
    print_step(6, "Configure Services")
    configure = input("\nConfigure OAuth credentials now? (Y/n): ").lower()
    if configure != 'n':
        configure_env()
    else:
        print("⏭️  Skipped OAuth configuration")
        print("   You can edit .env manually later")

    # Final summary
    print_header("Setup Complete!")

    print("Next steps:")
    print()

    if not has_google:
        print("❗ 1. Set up Google OAuth credentials")
        print("      See QUICKSTART.md for instructions")
        print()

    print("📝 2. Review and edit .env file with your credentials")
    print("      nano .env")
    print()

    print("🚀 3. Start the dashboard:")
    print("      python app.py")
    print("      or")
    print("      ./run.sh")
    print()

    print("🌐 4. Open http://localhost:5000 in your browser")
    print()

    print("📚 For detailed help, see README.md and QUICKSTART.md")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
