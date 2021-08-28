import discord
from discord.ext import commands
from utils import checks
from main import db
from utils.helpers import *
from datetime import datetime

class MainQuest(commands.Cog, name='MainQuest Commands'):
    """
  Commands for the managing MainQuest Stuff
  """

    def __init__(self, bot):
        self.bot = bot

    @checks.is_admin()
    @commands.command(name='complete_quest')
    async def complete_quest(self, ctx, member, quest: int):
        """
            Gives Main Quest  to a Member
        """
        await ctx.message.delete()
        member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        db.RobBot.MainQuest.update_one(f, {'$inc': {'MainQuest': quest}}, upsert=True)
        insert_transaction(ctx,'complete_quest', quest, f)
        await ctx.send(f'{member.display_name} completes Main Quest #{quest}')

    @commands.command(name='check_quest')
    async def check_quest(self, ctx, member = None):
        """
            Checks MQ of a member
        """
        await ctx.message.delete()
        if not member:
            member = ctx.author
        else:
            member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        t = await db.RobBot.MainQuest.find_one(f)
        await ctx.send(f'{member.display_name} has Main Quest# {t["MainQuest"]} completed')

    @checks.is_admin()
    @commands.command(name='remove_quest')
    async def remove_quest(self, ctx, member, quest: int):
        """
            Takes Main Quest  to a Member
        """
        await ctx.message.delete()
        member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        db.RobBot.MainQuest.update_one(f, {'$dec': {'MainQuest': quest}}, upsert=True)
        insert_transaction(ctx,'remove_quest', quest, f)
        await ctx.send(f'{member.display_name} Loses {quest} Main Quest')

def setup(bot):
    bot.add_cog(MainQuest(bot))
