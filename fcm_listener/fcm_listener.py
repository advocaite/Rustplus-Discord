# fcm_listener/fcm_listener.py

from rustplus import FCMListener
import json
import logging

# Initialize logger
logger = logging.getLogger('fcm_listener')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('fcm_listener.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class FCMListenerWrapper(FCMListener):
    def __init__(self, fcm_details, discord_bot):
        super().__init__(fcm_details)
        self.discord_bot = discord_bot

    def on_notification(self, obj, notification, data_message):
        # For now, dump the received data to a JSON file
        with open('fcm_data.json', 'a') as json_file:
            json.dump({'notification': notification, 'data_message': data_message}, json_file)
            json_file.write('\n')
        logger.info('Received FCM notification and saved to fcm_data.json.')
