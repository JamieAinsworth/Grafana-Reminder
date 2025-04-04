import os
from datetime import datetime
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables
load_dotenv()
client = WebClient(token=os.environ['SLACK_TOKEN'])
reminder_channel_id = os.environ['REMINDER_CHANNEL_ID'] # Reminder channel ID ds_turing
audit_channel_id = os.environ['AUDIT_CHANNEL_ID']
communication_channel_id = os.environ['COMMUNICATION_CHANNEL_ID']
group_id = os.environ['GROUP_ID'] # @Jamie

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
        print(f"Error fetching messages from channel {channel_id}: {e.response['error']}")
        return False

def send_reminder(missing_channels):
    try:
        if len(missing_channels) == 2:
            message = f"<@{group_id}> Grafana Monitoring missing for: " f"<#" + audit_channel_id + "> & <#" + communication_channel_id + ">"
        elif len(missing_channels) == 1:
            message = f"<@{group_id}> Grafana Monitoring missing for: {missing_channels[0]}."
        else:
            print("All channels have messages containing 'Grafana' for today. No reminder needed.")
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