from openai import OpenAI


class BanterBox:
    '''
    Interface between ChatGPT language models and PAL9000.
    '''
    def __init__(self, api_key):
        self.key = api_key
        self.client = OpenAI(api_key = self.key)
