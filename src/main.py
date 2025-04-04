from src.config import load_config
from src.grafana_checker import check_channels_for_grafana
from src.reminder import send_reminder

if __name__ == "__main__":
    config = load_config()
    missing_channels = check_channels_for_grafana(config)
    send_reminder(config, missing_channels)