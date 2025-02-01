import tweepy
import time
import random
import logging
from functools import wraps
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, TWITTER_USER_ID, BEARER_TOKEN

def exponential_backoff(retries=5, initial_delay=1, backoff_factor=2, jitter=True):
    """
    A retry decorator with exponential backoff.

    Args:
        retries (int): Maximum number of retry attempts.
        initial_delay (int): Initial delay in seconds.
        backoff_factor (int): Multiplier for exponential backoff.
        jitter (bool): If True, adds random jitter to delay.

    Returns:
        Decorator function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except tweepy.errors.TooManyRequests as e:
                    # Handle rate limit (429)
                    reset_time = int(e.response.headers.get("x-rate-limit-reset", time.time() + delay))
                    wait_time = reset_time - time.time()
                    logging.warning(f"Rate limit hit. Sleeping until reset: {wait_time:.2f} seconds.")
                    time.sleep(wait_time)
                except tweepy.errors.TweepyException as e:
                    logging.error(f"Error: {e}. Retrying in {delay:.2f} seconds (attempt {attempt}/{retries})...")
                    time.sleep(delay + (random.uniform(0, 1) if jitter else 0))
                    delay *= backoff_factor
                except Exception as e:
                    logging.error(f"Unexpected error: {e}. Retrying in {delay:.2f} seconds (attempt {attempt}/{retries})...")
                    time.sleep(delay + (random.uniform(0, 1) if jitter else 0))
                    delay *= backoff_factor
            raise Exception(f"Failed after {retries} retries.")
        return wrapper
    return decorator

def get_twitter_client():
    """
    Initialize and return the appropriate Tweepy client.
    Returns:
        tweepy.Client or tweepy.API
    """
    return tweepy.Client(bearer_token=BEARER_TOKEN)

@exponential_backoff(retries=5, initial_delay=2)
def get_original_tweets(client, max_results=5):
    """
    Fetch original tweets from the specified user (excludes retweets & replies).
    Returns a list of Tweet objects.

    Args:
        client: Tweepy client.
        max_results (int): Number of tweets to fetch.

    Returns:
        List of Tweet objects.
    """
    response = client.get_users_tweets(
            id=TWITTER_USER_ID,
            exclude=["retweets", "replies"],
            max_results=5,
            tweet_fields=["conversation_id", "created_at"]
        )
    return response.data if response.data else []

@exponential_backoff(retries=5, initial_delay=2)
def get_replies_in_thread(client, tweet_id, username, max_results=50):
    """
    Fetch replies from the same user in the same conversation (thread).

    Args:
        client: Tweepy client.
        tweet_id: ID of the original tweet.
        username: Twitter username.
        max_results (int): Number of replies to fetch.

    Returns:
        List of Tweet objects.
    """
    query = f"from:{username} conversation_id:{tweet_id}"
    response = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        tweet_fields=["conversation_id", "created_at"]
    )
    return response.data if response.data else []