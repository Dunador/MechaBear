import discord
from discord.ext import commands
from utils import checks
from main import db


class MemberTokens(commands.Cog, name='Token Commands'):
    """
  Commands for the managing tokens
  """

    def __init__(self, bot):
        self.bot = bot

    @checks.is_admin()
    @commands.command(name='give_token')
    async def give_token(self, ctx, member: discord.Member, tokens: int):
        """
            Gives tokens to a Member
        """
        f = {'member_id': member.id, 'server_id': ctx.guild.id}
        db.RobBot.tokens.update_one(f, {'$inc': {'tokens': tokens}}, upsert=True)
        await ctx.send(f'{ctx.author.display_name} gave {tokens} tokens to {member.display_name}')

    @commands.command(name='check_tokens')
    async def check_tokens(self, ctx, member: discord.Member = None):
        """
            Checks tokens of a member
        """
        if not member:
            member = ctx.author
        f = {'member_id': member.id, 'server_id': ctx.guild.id}
        t = await db.RobBot.tokens.find_one(f)
        await ctx.send(f'{member.display_name} has {t["tokens"]} tokens')


def setup(bot):
    bot.add_cog(MemberTokens(bot))
