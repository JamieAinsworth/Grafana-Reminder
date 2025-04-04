# Grafana Reminder Bot

[![Run Slack Bot](https://github.com/JamieAinsworth/Grafana-Reminder/actions/workflows/run-reminder.yml/badge.svg)](https://github.com/JamieAinsworth/Grafana-Reminder/actions/workflows/run-reminder.yml)

This project automates sending reminder messages in Slack by checking for recent posts in specified channels for the word "Grafana." If no recent posts contain that word, a reminder message is sent to a designated channel.

## Project Structure

```
Grafana-Reminder 
├── src
│   ├── turingGrafanaReminder.py  # Main script for automating reminders
├── .env                          # Environment variables (e.g., Slack API token)
├── requirements.txt              # Project dependencies
├── .github
│   └── workflows
│       └── run-slack-bot.yml     # GitHub Actions workflow for automation
└── README.md                     # Project documentation
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Grafana-Reminder
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and add your Slack API token:
```plaintext
SLACK_TOKEN=your_slack_api_token
```

### 5. Run the Script Locally
To manually run the reminder bot, execute the following command:
```bash
python src/turingGrafanaReminder.py
```

The bot will:
- Check for recent messages in the `#sbc_audit_service` and `#sbc_communication_service` channels for the word "Grafana."
- If no messages are found, it will send a reminder to the `#ds_turing` channel and mention the `@turing-squad` user group.

## Automation with GitHub Actions

The bot is configured to run automatically every weekday at **10:15 AM GMT** using GitHub Actions.

### Workflow File
The workflow file is located at `.github/workflows/run-slack-bot.yml`. It:
1. Runs the bot script on a schedule (Monday to Friday at 10:15 AM GMT).
2. Installs dependencies and executes the script.

### Setting Up GitHub Secrets
To securely store your Slack API token:
1. Go to your GitHub repository.
2. Navigate to **Settings** > **Secrets and variables** > **Actions**.
3. Add a new secret:
   - **Name**: `SLACK_TOKEN`
   - **Value**: Your Slack API token.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
