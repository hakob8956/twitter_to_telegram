import os
import logging

from config import PROCESSED_TWEETS_FILE

def load_processed_ids():
    """
    Load processed tweet IDs from a text file into a set.
    Returns an empty set if file doesn't exist.
    """
    if not os.path.exists(PROCESSED_TWEETS_FILE):
        return set()
    with open(PROCESSED_TWEETS_FILE, "r") as f:
        ids = f.read().strip().split()
        return set(ids)

def save_processed_id(tweet_id):
    """
    Append a processed tweet ID to the text file.
    """
    with open(PROCESSED_TWEETS_FILE, "a") as f:
        f.write(str(tweet_id) + "\n")

def html_escape(text):
    """
    Escape HTML special characters in text.
    """
    return (text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\"", "&quot;"))

def format_tweet_for_telegram(tweet):
    """
    Convert a Tweet object into a text message suitable for Telegram.
    Escapes HTML special characters and ensures proper formatting.
    """
    try:
        # Escape the tweet text
        escaped_text = html_escape(tweet["text"])
        
        # Create properly escaped tweet link
        tweet_url = f'https://twitter.com/user/status/{tweet["id"]}'
        tweet_link = f'<a href="{tweet_url}">Go to tweet</a>'
        
        # Combine elements with proper formatting
        text_with_tag = f"{escaped_text}\n#x\n\n{tweet_link}"
        return text_with_tag
        
    except KeyError as e:
        logging.error(f"Invalid tweet object: missing key {e}")
        raise ValueError(f"Invalid tweet object: missing key {e}")
    except Exception as e:
        logging.error(f"Error formatting tweet: {e}")
        raise ValueError(f"Error formatting tweet: {e}")