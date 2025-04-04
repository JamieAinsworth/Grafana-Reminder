import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)

def send_reminder(config, missing_channels):
    """
    Sends a reminder to the Slack reminder channel if Grafana monitoring is missing.

    Args:
        config (dict): Configuration dictionary containing Slack tokens and channel IDs.
        missing_channels (list): List of channels missing Grafana monitoring messages.
    """
    client = WebClient(token=config['SLACK_TOKEN'])
    try:
        if len(missing_channels) == 2:
            message = f"<@{config['GROUP_ID']}> Grafana Monitoring missing for: " \
                      f"<#{config['AUDIT_CHANNEL_ID']}> & <#{config['COMMUNICATION_CHANNEL_ID']}>"
        elif len(missing_channels) == 1:
            message = f"<@{config['GROUP_ID']}> Grafana Monitoring missing for: {missing_channels[0]}."
        else:
            logger.info("All channels have messages containing 'Grafana' for today. No reminder needed.")
            return

        client.chat_postMessage(channel=config['REMINDER_CHANNEL_ID'], text=message)
        logger.info(f"Reminder sent to channel {config['REMINDER_CHANNEL_ID']}: {message}")
    except SlackApiError as e:
        logger.error(f"Error sending reminder: {e.response['error']}")