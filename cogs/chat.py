import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
import requests
from requests import Response
from lib import json_reader

JSON = json_reader.read('config/config.json')  # todo: move to the lib directory
API_URL = JSON['api_urls']['open_ai']['chat']
API_KEY = JSON['api_tokens']['open_ai']
PREFIX = JSON['commands']['prefix']
COMMAND = JSON['commands']['chat']


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


def post_prompt(prompt: str, ctx: Context) -> Response:
    """
    Post a prompt to OpenAI's API to generate an image.
    :param prompt: The prompt to send.
    :return: A response from the API.
    """
    headers: dict = {'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
    data: dict = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt, "name": (str(ctx.author.name))}]
    }
    return requests.post(API_URL, json=data, headers=headers)


class ChatCog(Cog):
    """
    Cog that will add functionality to the Juicecord bot to allow with chatting with ChatGPT3.5.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=COMMAND)
    @commands.has_permissions(administrator=True)
    async def chat(self, ctx: Context) -> None:
        """
        Generate an AI image by connecting with the OpenAI API.

        Command Example: !chat Hello, There!

        :param ctx: The context from discord containing the user information and input.
        """
        await ctx.send("Thinking of a response...")

        prompt: str = generate_prompt(ctx.message) + " limit to between 1 and 1,950 characters."
        print(f'{ctx.author}: {prompt}')

        try:
            ai_response: Response = post_prompt(prompt, ctx)
            try:
                status: str = ai_response.json()['created']
                print(ai_response.json())
                if status is not None:
                    await ctx.send(f'{ctx.author.mention}, {ai_response.json()["choices"][0]["message"]["content"]}')

            except KeyError:
                error: str = ai_response.json()['error']['message']
                await ctx.send(f'{ctx.author.mention}, {error}')

        except Exception as e:
            await ctx.send(f'{ctx.author.mention}, {e} :cry:')


async def setup(bot: Bot) -> None:
    """
    Function required for setting up a cog in the discord API.
    This adds a cog to the main bot calling Bot.load_extention.
    :param bot: The bot to add the cog to.
    """
    await bot.add_cog(ChatCog(bot))
