import discord
from discord.ext import commands
from utils import checks
from main import db
from utils.helpers import *
from datetime import datetime

class Guilds(commands.Cog, name='Guilds'):
    """
  Commands for the managing Guilds
  """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add_guild')
    async def add_guild(self, ctx, member, *guilds):
        """
            adds a guilds to your list
        """
        await ctx.message.delete()
        member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        guilds = list(guilds)
        for pc in guilds:
            db.RobBot.guilds.update_one(f, {'$push': {'guilds': pc}}, upsert=True)
        insert_transaction(ctx,'add_guild', guilds, f)
        await ctx.send(f'{ctx.author.display_name} adds {guilds} to their list')

    @commands.command(name='list_guilds')
    async def list_guilds(self, ctx, member = None):
        """
            Checks guilds of a member
        """
        await ctx.message.delete()
        if not member:
            member = ctx.author
        else:
            member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        t = await db.RobBot.guilds.find_one(f)
        await ctx.send(f'{member.display_name} has {t["guilds"]} as guilds')

    @commands.command(name='del_guild')
    async def del_guild(self, ctx, member, *guilds):
        """
            deletes a guild to your list
        """
        await ctx.message.delete()
        member = m_search(ctx, member)
        guilds = list(guilds)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        exist_g = await db.RobBot.guilds.find_one(f)
        for g in guilds:
            if g in exist_g['guilds']:
                exist_g['guilds'].remove(g)
        db.RobBot.guilds.update_one(f, {'$set': {'guilds': exist_g['guilds']}}, upsert=True)
        insert_transaction(ctx,'del_guild', guilds, f)
        await ctx.send(f'{ctx.author.display_name} modifies their guilds to {exist_g["guilds"]}')


def setup(bot):
    bot.add_cog(Guilds(bot))
