import os
import discord
from discord.ext.commands import Bot
from lib import json_reader

JSON = json_reader.read('config/config.json')
TOKEN = JSON['api_tokens']['discord']
PREFIX = JSON['commands']['prefix']
INTENTS = discord.Intents.all()

bot = Bot(command_prefix=PREFIX, intents=INTENTS)


async def load_cogs() -> None:
    """
    Load all the cogs within the 'cogs/' directory into Juicecord.
    Each of these cogs serves as an extention of Juicecord adding a certain level of functionality.
    """
    print("Loading cogs...")
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"{filename[:-3]} added as an extension to Juicecord.")


@bot.event
async def on_ready() -> None:
    """
    Print on to the console when Juicecord is ready.
    """
    await load_cogs()
    print(f'{bot.user} has connected to Discord!')


bot.run(TOKEN)
