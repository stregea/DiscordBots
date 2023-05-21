import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
import requests
from requests import Response
import random
from lib.settings import IMAGE_COMMAND, IMAGE_API_URL
from lib.prompt import generate_prompt, post_prompt


def download_image(image_response: dict) -> str:
    """
    Download an image from a url based on a Response.

    :param image_response: The response containing the URL with the image to download.
    :return: The name of the image.
    """
    img_name = f"{random.randint(0, 999999999)}.png"
    img_data = requests.get(image_response['data'][0]['url']).content

    with open(img_name, 'wb') as handler:
        handler.write(img_data)

    return img_name


def delete_image(image_name: str):
    """
    Delete the local image from

    :param image_name:
    """
    if os.path.exists(image_name):
        os.remove(image_name)


class ImageDownloaderCog(Cog):
    """
    Cog that will add functionality to the Juicecord bot to download AI generated images from OpenAI.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=IMAGE_COMMAND)
    # @commands.has_permissions(administrator=True)
    async def generate_image(self, ctx: Context) -> None:
        """
        Generate an AI image by connecting with the OpenAI API.

        Command Example: !img Dog dancing

        :param ctx: The context from discord containing the user information and input.
        """
        await ctx.send(f'{ctx.author.mention}, generating your image...')

        prompt: str = generate_prompt(IMAGE_COMMAND, ctx.message)
        print(f'{ctx.author}: {prompt}')

        data: dict = {
            'prompt': prompt,
            'n': 1,
            'size': "512x512"
        }

        try:
            ai_response: Response = post_prompt(IMAGE_API_URL, data)
            try:
                response: dict = ai_response.json()
                status: str = response['created']

                if status is not None:
                    img_name: str = download_image(response)

                    await ctx.send(f'{ctx.author.mention} your image has generated!', file=discord.File(img_name))
                    delete_image(img_name)

            except KeyError:
                error: str = ai_response.json()['error']['message']
                await ctx.send(f'{ctx.author.mention}, {error}')

        except Exception:
            await ctx.send(f'{ctx.author.mention}, unable to create your image :cry:')


async def setup(bot: Bot) -> None:
    """
    Function required for setting up a cog in the discord API.
    This adds a cog to the main bot calling Bot.load_extension.

    :param bot: The bot to add the cog to.
    """
    await bot.add_cog(ImageDownloaderCog(bot))
