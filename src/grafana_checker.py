from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def check_channels_for_grafana(config: Dict[str, str]) -> List[str]:
    """
    Checks multiple Slack channels for messages containing the word 'Grafana' from today.

    Args:
        config (dict): Configuration dictionary containing Slack tokens and channel IDs.

    Returns:
        list: A list of channel names that are missing Grafana messages.
    """
    client = WebClient(token=config['SLACK_TOKEN'])
    channels_to_check = {
        config['AUDIT_CHANNEL_ID']: f"<#{config['AUDIT_CHANNEL_ID']}>",
        config['COMMUNICATION_CHANNEL_ID']: f"<#{config['COMMUNICATION_CHANNEL_ID']}>"
    }
    missing_channels = []

    for channel_id, channel_name in channels_to_check.items():
        if not check_channel_for_grafana(client, channel_id):
            missing_channels.append(channel_name)
    return missing_channels

def check_channel_for_grafana(client: WebClient, channel_id: str) -> bool:
    """
    Checks a single Slack channel for messages containing the word 'Grafana' from today.

    Args:
        client (WebClient): Slack WebClient instance.
        channel_id (str): The ID of the Slack channel to check.

    Returns:
        bool: True if a message containing 'Grafana' is found, False otherwise.
    """
    try:
        history = client.conversations_history(channel=channel_id, limit=100)
        messages = history.get('messages', [])
        today = datetime.now().date()
        for message in messages:
            message_date = datetime.fromtimestamp(float(message['ts'])).date()
            if message_date == today and "grafana" in message.get('text', '').lower():
                return True
        return False
    except SlackApiError as e:
        logger.error(f"Error fetching messages from channel {channel_id}: {e.response['error']}")
        return False