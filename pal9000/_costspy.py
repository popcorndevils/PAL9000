import os
import datetime
import json

from discord.interactions import Interaction
from openai.types.images_response import ImagesResponse


class CostSpy:
    '''
    tracks and enumerates the usage of PAL9000 by the server users.
    '''
    def __init__(self, logfile = "api_log.json"):
        self.log_folder = "logs"
        self.logfile = os.path.join(self.log_folder, logfile)
        self.initialize_log_file()

    def initialize_log_file(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)  # Create the logs directory if it doesn't exist
        if not os.path.exists(self.logfile):
            with open(self.logfile, 'w'):  # Create an empty log file if it doesn't exist
                pass

    def process(self, ctx: Interaction, response):
        if isinstance(response, ImagesResponse):
            with open(self.logfile, "a") as file:
                _log = {
                    "type": "dall-e-3",
                    "user": ctx.user.id,
                    "datetime": datetime.datetime.now().isoformat(),
                    "n": len(response.data),
                }
                file.writelines(json.dumps(_log) + "\n")

    def read_logs(self):
        try:
            with open(self.logfile, 'r') as file:
                return [json.loads(line) for line in file]

        except FileNotFoundError:
            print("Log file not found.")
