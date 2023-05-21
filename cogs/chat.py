from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
from requests import Response
from lib.settings import CHAT_COMMAND, CHAT_API_URL
from lib.prompt import generate_prompt, post_prompt


class ChatCog(Cog):
    """
    Cog that will add functionality to the Juicecord bot to allow with chatting with ChatGPT3.5.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=CHAT_COMMAND)
    # @commands.has_permissions(administrator=True)
    async def chat(self, ctx: Context) -> None:
        """
        Generate an AI image by connecting with the OpenAI API.

        Command Example: !chat Hello, There!

        :param ctx: The context from discord containing the user information and input.
        """
        await ctx.send(f'{ctx.author.mention}, thinking of a response...')

        prompt: str = f'{generate_prompt(CHAT_COMMAND, ctx.message)} limit to between 1 and 1,950 characters.'
        print(f'{ctx.author}: {prompt}')

        # Remove any spaces from a name that will break the OpenAPI regex.
        name: str = str(ctx.author.name).replace(' ', '')
        data: dict = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "name": name
                }
            ]
        }

        try:
            ai_response: Response = post_prompt(CHAT_API_URL, data)
            try:
                response: dict = ai_response.json()
                status: str = response['created']

                if status is not None:
                    message_content = response["choices"][0]["message"]["content"]
                    await ctx.send(f'{ctx.author.mention}, {message_content}')

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
