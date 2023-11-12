import os
import datetime
import json
import pandas as pd
from enum import Enum

from discord.interactions import Interaction
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.images_response import ImagesResponse
from ._types import ImageOptions, ChatGptChoices


class APIPrices:
    class ChatGPT4(Enum):
        # per 1000 tokens
        InputTokens = .03
        OutputTokens = .06

    class ChatGPT4_32k(Enum):
        # per 1000 tokens
        InputTokens = .06
        OutputTokens = .12

    class ChatGPT3_5_Turbo(Enum):
        # per 1000 tokens
        InputTokens = .0010
        OutputTokens = .0020

    class ChatGPT3_5_Turbo_Instruct(Enum):
        # per 1000 tokens
        InputTokens = .0015
        OutputTokens = .0020

    class DallE3:
        # per image
        class Standard(Enum):
            size_1024x1024 = .040
            size_1024x1792 = .080
            size_1792x1024 = .080

        class HD(Enum):
            size_1024x1024 = .080
            size_1024x1792 = .120
            size_1792x1024 = .120

    class DallE2(Enum):
        # per image
        size_1024x1024 = .020
        size_512x512 = .018
        size_256x256 = .016


price_map = {
    "gpt-4": APIPrices.ChatGPT4,
    "gpt-3.5-turbo": APIPrices.ChatGPT3_5_Turbo,
    "dall-e-3_standard_1024x1024": APIPrices.DallE3.Standard.size_1024x1024.value,
    "dall-e-3_standard_1792x1024": APIPrices.DallE3.Standard.size_1792x1024.value,
    "dall-e-3_standard_1024x1792": APIPrices.DallE3.Standard.size_1024x1792.value,
    "dall-e-3_hd_1024x1024": APIPrices.DallE3.HD.size_1024x1024.value,
    "dall-e-3_hd_1792x1024": APIPrices.DallE3.HD.size_1792x1024.value,
    "dall-e-3_hd_1024x1792": APIPrices.DallE3.HD.size_1024x1792.value,
    "dall-e-2_standard_1024x1024": APIPrices.DallE2.size_1024x1024.value,
    "dall-e-2_standard_512x512": APIPrices.DallE2.size_512x512.value,
    "dall-e-2_standard_256x256": APIPrices.DallE2.size_256x256.value,
}


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
        _df_others = _df[_df["user"] != _user_id]

        _user_stats = self.calc_usage(_df_usr)
        _others_stats = self.calc_usage(_df_others)

        # Print results
        print(_user_stats)
        print(_others_stats)

    def calc_usage(self, df):
        _df_chats = df[df["api_type"] == "chat_completion"]
        _df_images = df[df["api_type"] == "image_generation"]
        _df_images["cat"] = _df_images["model"] + "_" + _df_images["quality"] + "_" + _df_images["size"]

        _chat_usage = _df_chats.groupby('model').agg({'input_tokens': 'sum', 'completion_tokens': 'sum'}).to_dict('index')
        _chat_costs = {
            model: {
                "input_tokens": usage['input_tokens'],
                "output_tokens": usage['completion_tokens'],
                "input_cost": (usage['input_tokens'] / 1000) * price_map[model].InputTokens.value,
                "output_cost": (usage['completion_tokens'] / 1000) * price_map[model].OutputTokens.value
            }
            for model, usage in _chat_usage.items()
        }

        _img_usage = _df_images.groupby('cat').agg({'n': 'sum'}).to_dict('index')
        _img_costs = {
            cat: {
                "n": usage["n"],
                "cost": usage['n'] * price_map[cat]
            }
            for cat, usage in _img_usage.items()
        }
        return (_chat_costs, _img_costs)
