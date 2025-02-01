# twitter_to_telegram

## Description
`twitter_to_telegram` is a bot that periodically checks for new tweets from a specified Twitter account and posts them to a configured Telegram channel.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/twitter_to_telegram.git
    cd twitter_to_telegram
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Ensure you have configured the environment variables as described in the Configuration section.

2. Run the bot:
    ```sh
    python main.py
    ```

## Configuration
Create a [.env](http://_vscodecontentref_/1) file in the root directory of the project and add the following environment variables:

```env
# Twitter API Credentials
BEARER_TOKEN=your_bearer_token

# Telegram Bot API Credentials
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=your_telegram_channel_id
```
# Bot Settings
TWITTER_USER_ID=your_twitter_user_id
FETCH_INTERVAL_MINUTES=300  # Default to 300 minutes (5 hours)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.