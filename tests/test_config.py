import os
import unittest
from src.config import load_config

class TestConfig(unittest.TestCase):
    def setUp(self):
        # Set up mock environment variables
        os.environ['SLACK_TOKEN'] = 'test-slack-token'
        os.environ['REMINDER_CHANNEL_ID'] = 'test-reminder-channel'
        os.environ['AUDIT_CHANNEL_ID'] = 'test-audit-channel'
        os.environ['COMMUNICATION_CHANNEL_ID'] = 'test-communication-channel'
        os.environ['GROUP_ID'] = 'test-group-id'

    def tearDown(self):
        # Clear environment variables after each test
        os.environ.pop('SLACK_TOKEN', None)
        os.environ.pop('REMINDER_CHANNEL_ID', None)
        os.environ.pop('AUDIT_CHANNEL_ID', None)
        os.environ.pop('COMMUNICATION_CHANNEL_ID', None)
        os.environ.pop('GROUP_ID', None)

    def test_load_config_success(self):
        config = load_config()
        self.assertEqual(config['SLACK_TOKEN'], 'test-slack-token')
        self.assertEqual(config['REMINDER_CHANNEL_ID'], 'test-reminder-channel')

    def test_load_config_missing_variable(self):
        os.environ.pop('SLACK_TOKEN')
        with self.assertRaises(EnvironmentError):
            load_config()

if __name__ == '__main__':
    unittest.main()