import discord
from requests import post, Response
from lib.settings import API_KEY, PREFIX


def generate_prompt(command: str, message: discord.Message) -> str:
    """
    Based on a discord message, parse the text to generate a prompt to send to the API.

    :param command: The Juicecord command being performed.
    :param message: The discord message to parse.
    :return: A parsed message that serves as a prompt for the AI image generation.
    """
    # Remove the discord command.
    temp_command: list = [x for x in message.content.split(' ')]
    temp_command.remove(f'{PREFIX}{command}')
    ret = ""

    # Parse the input string
    for token in temp_command:
        ret += f"{token} "

    return ret


def post_prompt(api_url: str, data: dict) -> Response:
    """
    Post a prompt to OpenAI's API to generate an image.

    :param api_url: The url to send the request to.
    :param data: The data to send to the api.
    :return: A response from the API.
    """
    headers: dict = {'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
    return post(api_url, json=data, headers=headers)
