import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
import requests
from requests import Response
import random
from lib import json_reader

JSON = json_reader.read('config/config.json')
API_URL = JSON['api_urls']['open_ai']['image_generator']
API_KEY = JSON['api_tokens']['open_ai']
PREFIX = JSON['commands']['prefix']
COMMAND = JSON['commands']['generate_image']


def download_image(image_response: Response) -> str:
    """
    Download an image from a url based on a Response.
    :param image_response: The response containing the URL with the image to download.
    :return: The name of the image.
    """
    img_name = f"{random.randint(0, 999999999)}.png"
    img_data = requests.get(image_response.json()['data'][0]['url']).content

    with open(img_name, 'wb') as handler:
        handler.write(img_data)

    return img_name


def delete_image(image_name: str):
    """
    Delete the local image from
    :param image_name:
    :return:
    """
    if os.path.exists(image_name):
        os.remove(image_name)


def generate_prompt(message: discord.Message) -> str:
    """
    Based on a discord message, parse the text to generate a prompt to send to the API.
    :param message: The discord message to parse.
    :return: A parsed message that serves as a prompt for the AI image generation.
    """
    # Remove the discord command.
    command = [x for x in message.content.split(' ')]
    command.remove(f'{PREFIX}{COMMAND}')
    ret = ""

    # Parse the input string
    for token in command:
        ret += f"{token} "

    return ret


def post_prompt(prompt: str) -> Response:
    """
    Post a prompt to OpenAI's API to generate an image.
    :param prompt: The prompt to send.
    :return: A response from the API.
    """
    headers: dict = {'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
    data: dict = {
        'prompt': prompt,
        'n': 1,
        'size': "512x512"
    }

    return requests.post(API_URL, json=data, headers=headers)


class ImageDownloaderCog(Cog):
    """
    Cog that will add functionality to the Juicecord bot to download AI generated images from OpenAI.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=COMMAND)
    @commands.has_permissions(administrator=True)
    async def generate_image(self, ctx: Context) -> None:
        """
        Generate an AI image by connecting with the OpenAI API.

        Command Example: !img Dog dancing

        :param ctx: The context from discord containing the user information and input.
        """
        await ctx.send("Generating image...")

        prompt: str = generate_prompt(ctx.message)
        print(prompt)

        try:
            ai_response: Response = post_prompt(prompt)
            try:
                status: str = ai_response.json()['created']

                if status is not None:
                    img_name: str = download_image(ai_response)
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
    This adds a cog to the main bot calling Bot.load_extention.
    :param bot: The bot to add the cog to.
    """
    await bot.add_cog(ImageDownloaderCog(bot))
