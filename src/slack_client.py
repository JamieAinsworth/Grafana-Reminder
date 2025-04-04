from slack_sdk import WebClient

def get_slack_client(token):
    return WebClient(token=token)