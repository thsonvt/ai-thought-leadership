#!/usr/bin/env python3
"""
Notification Sender
Sends weekly digests via Email and Slack
"""

import os
import yaml
from pathlib import Path
from datetime import datetime
import requests

def load_notification_config():
    """Load notification configuration"""
    with open('config/notifications.yaml', 'r') as f:
        return yaml.safe_load(f)['notifications']

def load_latest_digest():
    """Load the most recent digest"""
    digest_dir = Path('content/synthesis/weekly-digests')

    # Find latest markdown file
    md_files = list(digest_dir.glob('*.md'))
    if not md_files:
        return None

    latest_file = max(md_files, key=lambda f: f.stat().st_mtime)

    # Load markdown content
    with open(latest_file, 'r') as f:
        content = f.read()

    # Load HTML version if exists
    html_file = latest_file.with_suffix('.html')
    html_content = None
    if html_file.exists():
        with open(html_file, 'r') as f:
            html_content = f.read()

    return {
        'week': latest_file.stem,
        'markdown': content,
        'html': html_content,
        'file': str(latest_file)
    }

def send_email(digest, config):
    """Send digest via email using SendGrid"""

    if not config.get('enabled', False):
        print("Email notifications disabled")
        return False

    # Check for SendGrid API key
    api_key = os.getenv('SENDGRID_API_KEY')
    if not api_key:
        print("⚠️  SENDGRID_API_KEY not set, skipping email")
        return False

    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        recipients = config.get('recipients', [])
        if not recipients:
            print("No email recipients configured")
            return False

        # Prepare email
        subject = f"{config.get('subject_prefix', '')} Weekly Digest - {digest['week']}"

        # Use HTML if available, otherwise convert markdown
        if digest['html']:
            content = digest['html']
        else:
            # Simple markdown to HTML conversion
            content = f"<pre>{digest['markdown']}</pre>"

        message = Mail(
            from_email=config.get('from_email', 'noreply@example.com'),
            to_emails=recipients,
            subject=subject,
            html_content=content
        )

        # Send via SendGrid
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        print(f"✅ Email sent (status {response.status_code})")
        print(f"   To: {', '.join(recipients)}")

        return True

    except Exception as e:
        print(f"❌ Email error: {e}")
        return False

def send_slack(digest, config):
    """Send digest via Slack webhook"""

    if not config.get('enabled', False):
        print("Slack notifications disabled")
        return False

    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("⚠️  SLACK_WEBHOOK_URL not set, skipping Slack")
        return False

    try:
        # Extract summary from markdown (first few lines)
        lines = digest['markdown'].split('\n')
        summary = '\n'.join(lines[:10])

        # Create Slack message
        payload = {
            "text": f"📚 Weekly AI Thought Leadership Digest - {digest['week']}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📚 Weekly Digest - {digest['week']}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": summary[:2900]  # Slack has char limits
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"AI Thought Leadership Knowledge Base • {datetime.now().strftime('%Y-%m-%d')}"
                        }
                    ]
                }
            ]
        }

        # Send to Slack
        response = requests.post(webhook_url, json=payload)

        if response.status_code == 200:
            print(f"✅ Slack notification sent")
            print(f"   Channel: {config.get('channel', '#general')}")
            return True
        else:
            print(f"❌ Slack error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Slack error: {e}")
        return False

def send_notifications_for_new_posts(new_posts, config):
    """Send simple notification about new posts (without digest)"""

    if not new_posts:
        return

    # Create simple summary
    summary = f"🆕 {len(new_posts)} new post(s) added to AI Thought Leadership KB:\n\n"
    for post in new_posts[:5]:  # Limit to 5
        summary += f"• {post}\n"

    # Send via Slack if enabled
    if config['slack'].get('enabled'):
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        if webhook_url:
            payload = {
                "text": summary[:2900]
            }
            try:
                requests.post(webhook_url, json=payload)
                print("✅ Slack notification sent for new posts")
            except:
                pass

def main():
    """Main notification function"""

    print("📬 Sending Notifications")
    print("=" * 50)

    # Load config
    config = load_notification_config()

    if not config.get('enabled', False):
        print("Notifications disabled in config")
        return

    # Load latest digest
    digest = load_latest_digest()

    if not digest:
        print("No digest found to send")
        return

    print(f"Digest: {digest['week']}")
    print(f"File: {digest['file']}")

    # Send notifications
    email_sent = send_email(digest, config['email'])
    slack_sent = send_slack(digest, config['slack'])

    print("\n" + "=" * 50)
    if email_sent or slack_sent:
        print("✅ Notifications sent successfully")
    else:
        print("⚠️  No notifications were sent")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Send digest notifications')
    parser.add_argument('--test', action='store_true', help='Test mode (check config)')

    args = parser.parse_args()

    if args.test:
        print("Testing notification configuration...")
        config = load_notification_config()
        print(f"Email enabled: {config['email'].get('enabled')}")
        print(f"Email recipients: {config['email'].get('recipients')}")
        print(f"Slack enabled: {config['slack'].get('enabled')}")
        print(f"SENDGRID_API_KEY set: {bool(os.getenv('SENDGRID_API_KEY'))}")
        print(f"SLACK_WEBHOOK_URL set: {bool(os.getenv('SLACK_WEBHOOK_URL'))}")
    else:
        main()
