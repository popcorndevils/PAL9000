import aiohttp
import discord
from random_word import RandomWords
from io import BytesIO
from configparser import ConfigParser
from discord.ext import commands

# Importing custom API handler classes
from ._pixelpainter import PixelPainter
from ._banterbox import BanterBox
from ._costspy import CostSpy


class Pal9000:
    def __init__(self, config: ConfigParser):
        # Initialize variables
        self.config = config
        self.random_words = RandomWords()
        self.whitelist = [v for v in self.config["WHITELIST"].values()]
        self.client = commands.Bot("/", intents=discord.Intents.all())

        # Initialize API helper classes
        self.painter = PixelPainter(config["AUTHORIZATION"]["OpenAIKey"])
        self.banter = BanterBox(config["AUTHORIZATION"]["OpenAIKey"])
        self.costspy = CostSpy()

        # Setup bot commands and events
        self.setup()

    def setup(self):
        @self.client.tree.command(name="gen", description="Create an image using DALL-E 3.")
        async def _gen(ctx: discord.interactions.Interaction, prompt: str):
            # Acknowledge interaction and check user authorization
            await ctx.response.defer()
            if self.check_user(ctx):
                response = self.painter.generate(prompt)
                self.costspy.process(ctx, response)

                # Asynchronous HTTP session to handle image download
                async with aiohttp.ClientSession() as session:
                    for image_data in response.data:
                        image_url = image_data.url  # Modify based on actual response structure
                        async with session.get(image_url) as resp:
                            if resp.status == 200:
                                data = await resp.read()
                                with BytesIO(data) as image_io:
                                    img_path = f'{self.random_words.get_random_word()}{self.random_words.get_random_word()}.png'
                                    # Send the image back to the user
                                    await ctx.followup.send(
                                        content=f"Here is the image you requested with this prompt: \n > {prompt}\n\nI have rewritten your prompt and submitted it to DALL-E 3 as:\n> \"{image_data.revised_prompt}\".\n",
                                        file=discord.File(image_io, img_path, description=img_path),
                                    )
                            else:
                                await ctx.response.send_message("Failed to download image.")
            else:
                await ctx.followup.send("You are not authorized to interact with me.")

        @self.client.event
        async def on_ready():
            # Set bot status and sync commands upon ready
            await self.client.change_presence(status=discord.Status.online)
            await self.client.tree.sync()
            print(f"Logged in as {self.client.user}")

    def check_user(self, ctx: discord.interactions.Interaction):
        # Check if user is in the whitelist
        return str(ctx.user.id) in self.whitelist

    def run(self):
        # Run the discord bot
        self.client.run(self.config["AUTHORIZATION"]["PAL9000Token"])
