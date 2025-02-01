import requests
import logging

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

def post_to_telegram(message):
    """
    Send a given message to the configured Telegram channel.
    """
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    response = requests.post(api_url, json=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error: {e}")
        logging.error(f"Response content: {response.content}")
        raise
    return response.json()