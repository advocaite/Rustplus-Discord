# discord_bot/bot.py

import discord
import logging
from rustplus import RustPlus

# Initialize logger
logger = logging.getLogger('discord_bot')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('discord_bot.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class DiscordBot:
    def __init__(self, token, channel_id, rustplus):
        self.token = token
        self.channel_id = channel_id
        self.client = discord.Client()
        self.rustplus = rustplus

    async def run(self):
        @self.client.event
        async def on_ready():
            logger.info('Logged in as {0.user}'.format(self.client))
            channel = self.client.get_channel(self.channel_id)
            await channel.send('Bot is now running!')

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            if message.content.startswith('!rustplus'):
                command = message.content[len('!rustplus'):].strip()
                logger.info(f'Received Rustplus command: {command}')

                # Execute Rustplus command
                try:
                    response = await self.rustplus.send_command(command)
                    await message.channel.send(f'Rustplus command executed successfully: {response}')
                except Exception as e:
                    await message.channel.send(f'Error executing Rustplus command: {e}')

        await self.client.start(self.token)
