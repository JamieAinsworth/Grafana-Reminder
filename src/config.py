import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    config = {
        'SLACK_TOKEN': os.getenv('SLACK_TOKEN'),
        'REMINDER_CHANNEL_ID': os.getenv('REMINDER_CHANNEL_ID'),
        'AUDIT_CHANNEL_ID': os.getenv('AUDIT_CHANNEL_ID'),
        'COMMUNICATION_CHANNEL_ID': os.getenv('COMMUNICATION_CHANNEL_ID'),
        'GROUP_ID': os.getenv('GROUP_ID'),
    }
    missing_vars = [key for key, value in config.items() if not value]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    return config