from discord.interactions import Interaction
from openai.types.images_response import ImagesResponse


class CostSpy:
    '''
    tracks and enumerates the usage of PAL9000 by the server users.
    '''
    def __init__(self):
        pass

    def process(self, ctx: Interaction, response):
        if isinstance(response, ImagesResponse):
            print("User generated an image")
