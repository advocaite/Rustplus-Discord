# rustplus_listener/listener.py

import asyncio
from rustplus import RustPlus
import logging

# Initialize logger
logger = logging.getLogger('rustplus_listener')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('rustplus_listener.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class RustplusListener:
    def __init__(self, server_address, server_port, auth_token, discord_bot):
        self.server_address = server_address
        self.server_port = server_port
        self.auth_token = auth_token
        self.discord_bot = discord_bot

    async def run(self):
        client = RustPlus(self.server_address, self.server_port)

        # Connect to the Rust server
        await client.connect()
        logger.info('Connected to Rust server.')

        # Send server info and connection stability message to Discord
        server_info = await client.get_server_info()
        if server_info:
            await self.discord_bot.post_server_info(server_info)
            await self.discord_bot.post_message("Connection to Rust server is stable.")
            logger.info('Server info sent to Discord.')

        # Keep the connection alive
        while True:
            await asyncio.sleep(1)
