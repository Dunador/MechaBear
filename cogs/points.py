import discord
from discord.ext import commands
from utils import checks
from main import db


class MemberPoints(commands.Cog, name='Points Commands'):
    """
  Commands for the managing points
  """

    def __init__(self, bot):
        self.bot = bot

    @checks.is_admin()
    @commands.command(name='give_points')
    async def give_points(self, ctx, member: discord.Member, points: int):
        """
            Gives tokens to a Member
        """
        f = {'member_id': member.id, 'server_id': ctx.guild.id}
        db.RobBot.points.update_one(f, {'$inc': {'points': points}}, upsert=True)
        await ctx.send(f'{ctx.author.display_name} gave {points} points to {member.display_name}')

    @commands.command(name='check_points')
    async def check_points(self, ctx, member: discord.Member = None):
        """
            Checks points of a member
        """
        if not member:
            member = ctx.author
        f = {'member_id': member.id, 'server_id': ctx.guild.id}
        t = await db.RobBot.points.find_one(f)
        await ctx.send(f'{member.display_name} has {t["points"]} points')


def setup(bot):
    bot.add_cog(MemberPoints(bot))
