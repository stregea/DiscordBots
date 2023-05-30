from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
from lib.settings import SMITE_COMMAND
from secrets import choice
from lib.prompt import generate_prompt


class SmiteCog(Cog):
    """
    Cog that will add functionality to the Juicecord bot to smite/insult members.
    """

    def __init__(self, bot):
        self.bot = bot

    def is_username_user_id(self, username: str) -> bool:
        """
        Determine if a username is instead a user id.

        :param username: The username to check.
        :return: True if the username was a mention (user id), False otherwise.
        """
        is_user_id = False
        user_id = username[2:-1]

        # determine if the user passed in a user id
        try:
            user_id = int(user_id)
            is_user_id = True
        except ValueError:
            pass

        return is_user_id

    def smite_users(self, ctx: Context) -> set:
        """
        Send messages out to insult members that were mentioned in a prompt.

        :param ctx: The context from discord containing the user information and input.
        """
        # todo: Have Juicecord ignore bot users.
        prompt = generate_prompt(SMITE_COMMAND, ctx.message).replace(' ', '')

        # todo: implement regex to handle spaces as well as 'and'.
        usernames = prompt.split(',')
        members: list = []
        if prompt == '@everyone':
            for member in ctx.guild.members:
                members.append(member)
        else:
            for username in usernames:

                is_user_id = self.is_username_user_id(username)

                # Add the current author if 'me' is sent in.
                if username.upper() == 'ME':
                    members.append(ctx.author)

                # Parse the user id if a mention was passed in.
                elif is_user_id:
                    # parse the user id
                    user_id: int = int(username[2:-1])
                    members.append(ctx.guild.get_member(user_id))

                # Otherwise parse the text and check if the text matches a member name.
                else:
                    for member in ctx.guild.members:
                        if username == member.name:
                            members.append(member)
                        elif username in member.name:
                            members.append(member)

        # Convert to a set to remove potential duplicates
        members_set: set = set()
        members_set.update(members)
        return members_set

    @commands.command(name=SMITE_COMMAND)
    # @commands.has_permissions(administrator=True)
    async def smite(self, ctx: Context) -> None:
        """
        Send funny insults to users within the Discord channel.

        Command Example: !smite me

        :param ctx: The context from discord containing the user information and input.
        """
        insults: list = []
        with open('lib/insults.txt') as file:
            insults = file.readlines()

        members = self.smite_users(ctx)

        for member in members:
            selected_insult = choice(insults)
            await ctx.send(f'{member.mention}, {selected_insult}')


async def setup(bot: Bot) -> None:
    """
    Function required for setting up a cog in the discord API.
    This adds a cog to the main bot calling Bot.load_extention.
    :param bot: The bot to add the cog to.
    """
    await bot.add_cog(SmiteCog(bot))
