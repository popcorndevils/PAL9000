from openai import OpenAI


class PixelPainter:
    '''
    Interface between OpenAI's DALL-E 3 API and PAL9000.
    '''
    def __init__(self, api_key):
        self.key = api_key
        self.client = OpenAI(api_key = self.key)

    def generate(self, prompt: str):
        response = self.client.images.generate(
            model = "dall-e-3",
            prompt = prompt,
            size = "1024x1024",
            quality = "standard",
            n = 1,
        )
        return response
