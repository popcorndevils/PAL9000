

class PixelPainter:
    '''
    Interface between OpenAI's DALL-E 3 API and PAL9000.
    '''
    def __init__(self, api_key):
        self.key = api_key
