import discord
import os
import json
import random
import requests
from discord.ext import commands

DISCORD_TOKEN = "MTA5OTgwMzc4NzExNzQ2MTYwNQ.G5BMKm.J7iMpHZuwXVjXEy5LcfPhNVFMoyxg8BZi5qu8Y"
API_KEY = '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'
PRE_FIX = '!'
COMMAND = 'img'

TOKEN = DISCORD_TOKEN
INTENTS = discord.Intents.all()

bot = commands.Bot(command_prefix=PRE_FIX, intents=INTENTS)


def download_image(image_response: requests.Response) -> str:
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


def generate_command_string(message: discord.Message) -> str:
    """
    Based on a discord message, parse the
    :param message:
    :return:
    """
    # Remove the discord command.
    command = [x for x in message.content.split(' ')]
    command.remove(f'{PRE_FIX}{COMMAND}')
    ret = ""

    # Parse the input string
    for token in command:
        ret += f"{token} "

    return ret


@bot.event
async def on_ready() -> None:
    """

    :return:
    """
    print(f'{bot.user} has connected to Discord!')


@bot.command(name=COMMAND)
async def generate_image(ctx: discord.ext.commands.Context):
    """
    Generate an AI image by connecting with the OpenAI API.

    Command Example: !img Dog dancing

    :param ctx: The context from discord containing the user information and input.
    :return:
    """
    await ctx.send("Generating image...")

    message_text = generate_command_string(ctx.message)
    print(message_text)

    data = {
        'prompt': message_text,
        'n': 1,
        'size': "512x512"
    }

    try:
        ai_request = requests.post(
            "https://api.openai.com/v1/images/generations",
            json=data,
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
        )

        try:
            status = ai_request.json()['created']

            if status is not None:
                img_name = download_image(ai_request)
                await ctx.send(f'{ctx.author.mention} your image has generated!', file=discord.File(img_name))
                delete_image(img_name)

        except KeyError:
            error = ai_request.json()['error']['message']
            await ctx.send(f'{ctx.author.mention}, {error}')

    except json.decoder.JSONDecodeError as e:
        await ctx.send(f'{ctx.author.mention}, unable to create your image :cry:')


bot.run(TOKEN)
