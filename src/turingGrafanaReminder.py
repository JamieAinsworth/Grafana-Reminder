import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
client = WebClient(token=os.environ['SLACK_TOKEN'])
reminder_channel_id = os.environ['REMINDER_CHANNEL_ID'] # Reminder channel ID ds_turing
audit_channel_id = os.environ['AUDIT_CHANNEL_ID']
communication_channel_id = os.environ['COMMUNICATION_CHANNEL_ID']
group_id = os.environ['GROUP_ID'] # @Jamie

required_env_vars = ['SLACK_TOKEN', 'REMINDER_CHANNEL_ID', 'AUDIT_CHANNEL_ID', 'COMMUNICATION_CHANNEL_ID', 'GROUP_ID']
for var in required_env_vars:
    if var not in os.environ:
        raise EnvironmentError(f"Missing required environment variable: {var}")

def retry_on_rate_limit(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SlackApiError as e:
            if e.response['error'] == 'rate_limited':
                retry_after = int(e.response.headers.get('Retry-After', 1))
                logger.warning(f"Rate limited. Retrying after {retry_after} seconds...")
                sleep(retry_after)
                return func(*args, **kwargs)
            else:
                raise e
    return wrapper

@retry_on_rate_limit
def check_channel_for_grafana(channel_id):
    try:
        # Fetch the message history from the channel
        history = client.conversations_history(channel=channel_id, limit=100)
        messages = history['messages']

        today = datetime.now().date()
        for message in messages:
            # Convert the message timestamp to a datetime object
            message_date = datetime.fromtimestamp(float(message['ts'])).date()

            # Check if the message is from today and contains the word "Grafana"
            if message_date == today and "grafana" in message.get('text', '').lower():
                return True  # Found a message with "Grafana"
        return False  # No messages with "Grafana" found today
    except SlackApiError as e:
        logger.error(f"Error fetching messages from channel {channel_id}: {e.response['error']}")
        return False

def send_reminder(missing_channels):
    try:
        if len(missing_channels) == 2:
            message = f"<@{group_id}> Grafana Monitoring missing for: " f"<#" + audit_channel_id + "> & <#" + communication_channel_id + ">"
        elif len(missing_channels) == 1:
            message = f"<@{group_id}> Grafana Monitoring missing for: {missing_channels[0]}."
        else:
            logger.info("All channels have messages containing 'Grafana' for today. No reminder needed.")
            return  # No reminder needed
        
        client.chat_postMessage(channel=reminder_channel_id, text=message)
        print(f"Reminder sent to channel {reminder_channel_id}: {message}")

    except SlackApiError as e:
        print(f"Error sending reminder: {e.response['error']}")

if __name__ == "__main__":
    # Channel IDs to check for "Grafana"
    channels_to_check = {
        audit_channel_id: "<#"+ audit_channel_id + ">",
        communication_channel_id: "<#" + communication_channel_id + ">"
    }
    missing_channels = []

    # Check each channel for "Grafana"
    for channel_id, channel_name in channels_to_check.items():
        if not check_channel_for_grafana(channel_id):
            missing_channels.append(channel_name)

    # Send a reminder if needed
    send_reminder(missing_channels)