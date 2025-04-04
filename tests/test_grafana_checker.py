import unittest
from unittest.mock import MagicMock
from src.grafana_checker import check_channels_for_grafana, check_channel_for_grafana

class TestGrafanaChecker(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.config = {
            'SLACK_TOKEN': 'test-slack-token',
            'AUDIT_CHANNEL_ID': 'test-audit-channel',
            'COMMUNICATION_CHANNEL_ID': 'test-communication-channel',
        }

    def test_check_channel_for_grafana_found(self):
        # Mock Slack API response with a message containing "Grafana"
        self.mock_client.conversations_history.return_value = {
            'messages': [{'ts': '1234567890.123', 'text': 'Grafana alert!'}]
        }
        result = check_channel_for_grafana(self.mock_client, 'test-audit-channel')
        self.assertTrue(result)

    def test_check_channel_for_grafana_not_found(self):
        # Mock Slack API response with no "Grafana" messages
        self.mock_client.conversations_history.return_value = {
            'messages': [{'ts': '1234567890.123', 'text': 'No alerts today.'}]
        }
        result = check_channel_for_grafana(self.mock_client, 'test-audit-channel')
        self.assertFalse(result)

    def test_check_channels_for_grafana(self):
        # Mock Slack API responses for multiple channels
        self.mock_client.conversations_history.side_effect = [
            {'messages': [{'ts': '1234567890.123', 'text': 'Grafana alert!'}]},
            {'messages': [{'ts': '1234567890.123', 'text': 'No alerts today.'}]}
        ]
        result = check_channels_for_grafana(self.config)
        self.assertEqual(result, ['<#test-communication-channel>'])

if __name__ == '__main__':
    unittest.main()