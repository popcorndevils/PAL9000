from openai import OpenAI
from ._types import ChatLogs


class BanterBox:
    '''
    Interface between ChatGPT language models and PAL9000.
    '''
    def __init__(self, api_key):
        self.key = api_key
        self.client = OpenAI(api_key = self.key)

    def ask(self, ctx, log: ChatLogs):
        self.client.chat.completions.create(
            model = "gpt-3.5.turbo",
            messages = log.to_data(),
        )
