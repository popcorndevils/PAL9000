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
from ._types import ImageOptions, ImageCommandChoices, ChatGptChoices, ChatProfiles
from ._types._chatmessage import Roles


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
        @self.client.tree.command(name="gen", description="Create images using DALL-E.")
        async def _gen(
            ctx: discord.interactions.Interaction,
            prompt: str,
            silent: bool = True,
            n: int = 1,
            size: ImageCommandChoices.ImageSize = ImageCommandChoices.ImageSize.size_1024x1024,
            quality: ImageCommandChoices.ImageQuality = ImageCommandChoices.ImageQuality.standard,
            model: ImageCommandChoices.DallEModel = ImageCommandChoices.DallEModel.dall_e_3,
        ):

            _image_options = ImageOptions(model, quality, size, n)

            # Acknowledge interaction and check user authorization
            await ctx.response.defer()
            try:
                if self.check_user(ctx):
                    n = n if n <= 4 else 4
                    response = await self.painter.generate_multiple(prompt, _image_options)
                    self.costspy.process(ctx, response, options = _image_options)

                    # Asynchronous HTTP session to handle image download
                    async with aiohttp.ClientSession() as session:
                        _files = []
                        for image_data in response.data:
                            image_url = image_data.url  # Modify based on actual response structure
                            async with session.get(image_url) as resp:
                                if resp.status == 200:
                                    data = await resp.read()
                                    _files.append(discord.File(
                                        BytesIO(data),
                                        f'{self.random_words.get_random_word()}{self.random_words.get_random_word()}.png'))
                        if not silent:
                            await ctx.followup.send(
                                content=f"\nHere is the image you requested with this prompt: \n > {prompt}\".\n",
                                files = _files)
                        else:
                            await ctx.followup.send(files = _files)
                else:
                    await ctx.followup.send("You are not authorized to interact with me.")
            except Exception as e:
                await ctx.followup.send(f"\nI'm sorry, your prompt was rejected due to the following error:\n\n> {e.message}")

        @self.client.tree.command(name="ask", description="Ask ChatGPT a quick question without chat context.")
        async def _ask(
            ctx: discord.interactions.Interaction,
            prompt: str,
            model: ChatGptChoices.ChatModel = ChatGptChoices.ChatModel.GPT_3_5_Turbo
        ):
            # Acknowledge interaction and check user authorization
            await ctx.response.defer()

            try:
                if self.check_user(ctx):
                    _question = ChatProfiles["default"]
                    _question.add_msg(Roles.user, prompt)
                    response = await self.banter.ask(_question)

                    self.costspy.process(ctx, response, chat_model = model)

                    await ctx.followup.send(response.choices[0].message.content)
                else:
                    await ctx.followup.send("You are not authorized to interact with me.")
            except Exception as e:
                await ctx.followup.send(f"\nI'm sorry, your prompt was rejected due to the following error:\n\n> {e.message}")

        @self.client.tree.command(name="usage", description="Retrieve Bot usage statistics.")
        async def _usage(
            ctx: discord.interactions.Interaction
        ):
            # Acknowledge interaction and check user authorization
            await ctx.response.defer()

            try:
                if self.check_user(ctx):
                    self.costspy.generate_usage_stats(ctx)
                    await ctx.followup.send("Things were calculated.")
                else:
                    await ctx.followup.send("You are not authorized to interact with me.")
            except Exception as e:
                await ctx.followup.send(f"\nI'm sorry, there was a problem:\n\n> {e.message}")

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
