import discord
from discord.ext import commands


class UserCommands(commands.Cog, name='User Commands'):
    """
    User Commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test', aliases=['tst'])
    async def test(self, ctx):
        """
        Runs a test command
        """
        await ctx.message.delete()
        await ctx.send('Done')  # Sends a message where content='Done'


def setup(bot):
    bot.add_cog(UserCommands(bot))
