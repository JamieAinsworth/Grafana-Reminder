import unittest
from unittest.mock import MagicMock
from src.reminder import send_reminder

class TestReminder(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.config = {
            'SLACK_TOKEN': 'test-slack-token',
            'REMINDER_CHANNEL_ID': 'test-reminder-channel',
            'AUDIT_CHANNEL_ID': 'test-audit-channel',
            'COMMUNICATION_CHANNEL_ID': 'test-communication-channel',
            'GROUP_ID': 'test-group-id',
        }

    def test_send_reminder_two_channels(self):
        send_reminder(self.config, ['<#test-audit-channel>', '<#test-communication-channel>'])
        self.mock_client.chat_postMessage.assert_called_once_with(
            channel='test-reminder-channel',
            text="<@test-group-id> Grafana Monitoring missing for: <#test-audit-channel> & <#test-communication-channel>"
        )

    def test_send_reminder_one_channel(self):
        send_reminder(self.config, ['<#test-audit-channel>'])
        self.mock_client.chat_postMessage.assert_called_once_with(
            channel='test-reminder-channel',
            text="<@test-group-id> Grafana Monitoring missing for: <#test-audit-channel>."
        )

    def test_send_reminder_no_channels(self):
        send_reminder(self.config, [])
        self.mock_client.chat_postMessage.assert_not_called()

if __name__ == '__main__':
    unittest.main()