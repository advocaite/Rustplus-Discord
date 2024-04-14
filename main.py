# main.py

import logging
import asyncio
import json

from discord_bot.bot import DiscordBot
from rustplus_listener.listener import RustplusListener
from fcm_listener.fcm_listener import FCMListenerWrapper
from rustplus import RustPlus

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('discord_bot').setLevel(logging.DEBUG)
logging.getLogger('rustplus_listener').setLevel(logging.DEBUG)
logging.getLogger('fcm_listener').setLevel(logging.DEBUG)

# Your settings
DISCORD_TOKEN = 'your_discord_token_here'
DISCORD_CHANNEL_ID = 123456789012345678
RUSTPLUS_SERVER_ADDRESS = '127.0.0.1'
RUSTPLUS_SERVER_PORT = 28016
RUSTPLUS_AUTH_TOKEN = 'your_rustplus_auth_token_here'
FCM_CONFIG_FILE = 'rustplus.py.config.json'

async def main():
    # Initialize Rustplus client
    rustplus = RustPlus(RUSTPLUS_SERVER_ADDRESS, RUSTPLUS_SERVER_PORT, RUSTPLUS_AUTH_TOKEN)

    # Initialize Discord bot
    discord_bot = DiscordBot(DISCORD_TOKEN, DISCORD_CHANNEL_ID, rustplus)

    # Initialize Rustplus listener
    rustplus_listener = RustplusListener(RUSTPLUS_SERVER_ADDRESS, RUSTPLUS_SERVER_PORT, RUSTPLUS_AUTH_TOKEN, discord_bot)

    # Read FCM details from config file
    with open(FCM_CONFIG_FILE, 'r') as fcm_config_file:
        fcm_details = json.load(fcm_config_file)

    # Initialize FCM listener
    fcm_listener = FCMListenerWrapper(fcm_details, discord_bot)

    # Run Discord bot, Rustplus listener, and FCM listener concurrently
    await asyncio.gather(
        discord_bot.run(),
        rustplus_listener.run(),
        fcm_listener.start()
    )

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
