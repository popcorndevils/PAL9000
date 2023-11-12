import os
import datetime
import json
import pandas as pd

from discord.interactions import Interaction
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.images_response import ImagesResponse
from ._types import ImageOptions, ChatGptChoices
from ._pandabear import PandaBear


class CostSpy:
    '''
    tracks and enumerates the usage of PAL9000 by the server users.
    '''
    def __init__(self, logfile = "api_log.json"):
        self.pandabear = PandaBear()
        self.log_folder = "logs"
        self.logfile = os.path.join(self.log_folder, logfile)
        self.initialize_log_file()

    def initialize_log_file(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)  # Create the logs directory if it doesn't exist
        if not os.path.exists(self.logfile):
            with open(self.logfile, 'w'):  # Create an empty log file if it doesn't exist
                pass

    def process(self, ctx: Interaction, response, **kwargs):
        if isinstance(response, ImagesResponse) and "options" in kwargs and isinstance(kwargs["options"], ImageOptions):
            _options = kwargs["options"]
            with open(self.logfile, "a") as file:
                _log = _options.to_data()
                _log["api_type"] = "image_generation"
                _log["datetime"] = datetime.datetime.now().isoformat()
                _log["user"] = ctx.user.id
                file.writelines(json.dumps(_log) + "\n")

        elif isinstance(response, ChatCompletion) and "chat_model" in kwargs and isinstance(kwargs["chat_model"], ChatGptChoices.ChatModel):
            _model: ChatGptChoices.ChatModel = kwargs["chat_model"]
            with open(self.logfile, "a") as file:
                _log = {
                    "api_type": "chat_completion",
                    "datetime": datetime.datetime.now().isoformat(),
                    "user": ctx.user.id,
                    "model": _model.value,
                    "input_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                }
                file.writelines(json.dumps(_log) + "\n")

    def read_logs(self):
        try:
            with open(self.logfile, 'r') as file:
                return pd.DataFrame([json.loads(line) for line in file])

        except FileNotFoundError:
            print("Log file not found.")

    def generate_usage_stats(self, ctx: Interaction):
        _df = self.read_logs()

        _user_id = ctx.user.id
        _df_usr = _df[_df["user"] == _user_id]
        _user_stats: pd.DataFrame = self.pandabear.calc_usage(_df_usr)

        # _df_others = _df[_df["user"] != _user_id]
        # _others_stats: pd.DataFrame = self.pandabear.calc_usage(_df_others)

        return _user_stats
