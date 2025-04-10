# Grafana Reminder Bot

[![Run Slack Bot](https://github.com/JamieAinsworth/Grafana-Reminder/actions/workflows/run-reminder.yml/badge.svg)](https://github.com/JamieAinsworth/Grafana-Reminder/actions/workflows/run-reminder.yml)

This project automates sending reminder messages in Slack by checking for recent posts in specified channels for the word "Grafana." If no recent posts contain that word, a reminder message is sent to a designated channel.

## Project Structure

```
Grafana-Reminder 
├── src
│   ├── turingGrafanaReminder.py  # Main script for automating reminders
│   └── rota
│       └── rota.json             # Weekly rota for main and backup responsibilities
├── .env                          # Environment variables (e.g., Slack API token and user IDs)
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
Create a `.env` file in the root directory and add your Slack API token and user IDs:
```plaintext
SLACK_TOKEN=your_slack_api_token
REMINDER_CHANNEL_ID=your_reminder_channel_id
AUDIT_CHANNEL_ID=your_audit_channel_id
COMMUNICATION_CHANNEL_ID=your_communication_channel_id

# User IDs for rota members
JAMIE_ID=slack_user_id
ANAND_ID=slack_user_id
BEN_ID=slack_user_id
KHUSHBU_ID=slack_user_id
MOSES_ID=slack_user_id
JOHN_ID=slack_user_id
UTTAM_ID=slack_user_id
DALE_ID=slack_user_id
MOHIT_ID=slack_user_id
DHRUV_ID=slack_user_id
```

### 5. Add the Rota File
Ensure the `rota.json` file is located in the `src/rota` directory. This file contains the weekly rota for main and backup responsibilities:
```json
[
    {
        "week_commencing": "07 April 2025",
        "main": "Jamie",
        "backup": "Anand"
    },
    {
        "week_commencing": "14 April 2025",
        "main": "Jamie",
        "backup": "Ben"
    }
    // Add more weeks as needed
]
```

### 6. Run the Script Locally
To manually run the reminder bot, execute the following command:
```bash
python src/turingGrafanaReminder.py
```

The bot will:
- Check for recent messages in the specified channels for the word "Grafana."
- If no messages are found, it will send a reminder to the designated channel and mention the main and backup users for the current week.

## Automation with GitHub Actions

The bot is configured to run automatically every weekday at **10:15 AM GMT** using GitHub Actions.

### Workflow File
The workflow file is located at `.github/workflows/run-slack-bot.yml`. It:
1. Runs the bot script on a schedule (Monday to Friday at 10:15 AM GMT).
2. Installs dependencies and executes the script.

### Setting Up GitHub Secrets
To securely store your Slack API token and other sensitive data:
1. Go to your GitHub repository.
2. Navigate to **Settings** > **Secrets and variables** > **Actions**.
3. Add new secrets:
   - **Name**: `SLACK_TOKEN`
   - **Value**: Your Slack API token.
   - **Name**: `REMINDER_CHANNEL_ID`, `AUDIT_CHANNEL_ID`, `COMMUNICATION_CHANNEL_ID`, etc.
   - **Value**: Corresponding channel IDs.

## Recent Updates
- **Rota Integration**: The bot now uses a `rota.json` file to determine the main and backup responsible for the current week.
- **Dynamic Slack ID Retrieval**: Slack user IDs are stored in the `.env` file and retrieved dynamically using the `get_slack_id` function.
- **Error Handling**: Improved error handling for missing rota entries and Slack API errors.
