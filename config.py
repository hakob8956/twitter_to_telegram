import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Twitter (X) API Credentials
BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # For OAuth 2.0 Application-Only

# Telegram Bot API Credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")  # e.g., "-1001234567890"

# Bot Settings
TWITTER_USER_ID = os.getenv("TWITTER_USER_ID")  # Numeric user ID for the account to track
FETCH_INTERVAL_MINUTES = int(os.getenv("FETCH_INTERVAL_MINUTES", 300))  # Default to 300 minutes (5 hours)

# File to store processed tweet IDs
PROCESSED_TWEETS_FILE = "processed_tweets.txt"
