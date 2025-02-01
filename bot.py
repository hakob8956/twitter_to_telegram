import time
import logging

from config import (
    FETCH_INTERVAL_MINUTES,
    TWITTER_USER_ID,
)
from twitter_api import get_twitter_client, get_original_tweets, get_replies_in_thread
from telegram_api import post_to_telegram
from processing import load_processed_ids, save_processed_id, format_tweet_for_telegram

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[
    logging.FileHandler("bot.log"),
    logging.StreamHandler()
])

def run_bot():
    """
    The main loop for periodically checking new tweets, posting them to Telegram,
    and handling their replies (threads).
    """
    client = get_twitter_client()
    processed_ids = load_processed_ids()

    while True:
        logging.info("Checking for new tweets...")

        try:
            # Fetch original tweets
            original_tweets = get_original_tweets(client, max_results=10)
            if original_tweets is None:
                logging.info("No new tweets found or an error occurred.")
            else:
                # Sort them ascending by created_at so older tweets get posted first
                original_tweets = sorted(original_tweets, key=lambda t: t.created_at, reverse=True)

                for tweet in original_tweets:
                    tweet_id_str = str(tweet.id)

                    if tweet_id_str in processed_ids:
                        # Already processed
                        continue

                    # Post the original tweet
                    message = format_tweet_for_telegram(tweet)
                    post_to_telegram(message)
                    logging.info(f"Posted tweet {tweet_id_str} to Telegram.")

                    # Mark as processed
                    save_processed_id(tweet_id_str)
                    processed_ids.add(tweet_id_str)

                    # Fetch your own replies to this tweet (the thread)
                    replies = get_replies_in_thread(client, tweet.id, TWITTER_USER_ID, max_results=50)
                    replies = sorted(replies, key=lambda r: r.created_at)

                    for reply_tweet in replies:
                        # Skip if it's the same as the original tweet or already processed
                        if reply_tweet.id == tweet.id:
                            continue

                        reply_id_str = str(reply_tweet.id)
                        if reply_id_str not in processed_ids:
                            reply_message = format_tweet_for_telegram(reply_tweet)
                            post_to_telegram(reply_message)
                            logging.info(f"Posted reply tweet {reply_id_str} to Telegram.")

                            save_processed_id(reply_id_str)
                            processed_ids.add(reply_id_str)
        except Exception as e:
            logging.error(f"Error occurred: {e}")

        logging.info(f"Sleeping for {FETCH_INTERVAL_MINUTES} minutes...")
        time.sleep(FETCH_INTERVAL_MINUTES * 60)