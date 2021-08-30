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
        self.add_color = discord.Colour.green()
        self.del_color = discord.Colour.red()
        self.info_color= discord.Colour.orange()

    @commands.command(name='add_guild')
    async def add_guild(self, ctx, member, *guilds):
        """
        Usage: add_guild [member(required)] [guilds]
        """
        await ctx.message.delete()
        member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        e = discord.Embed(title='Add a Guild',
                          type='rich',
                          description=f'{member.display_name}',
                          colour=self.add_color)
        e.set_footer(text=f'executed by: {ctx.author.display_name} ')
        e.set_thumbnail(url=member.avatar_url)
        guilds = list(guilds)
        guild_list = ''
        for pc in guilds:
            db.RobBot.guilds.update_one(f, {'$push': {'guilds': pc}}, upsert=True)
            guild_list += f'{pc}\n'
        e.add_field(name="Guild Added", value=guild_list)
        await insert_transaction(ctx,'add_guild', guilds, f)
        await ctx.send(embed=e)

    @commands.command(name='list_guilds', aliases=['lg'])
    async def list_guilds(self, ctx, member=None):
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
        e = discord.Embed(title='List Guilds',
                          type='rich',
                          description=f'{member.display_name}',
                          colour=self.info_color)
        e.set_footer(text=f'executed by: {ctx.author.display_name} ')
        e.set_thumbnail(url=member.avatar_url)
        guild_str = ''
        if not t['guilds']:
            e.add_field(name="Guilds", value="None")
        else:
            for guild in t['guilds']:
                guild_str += f'{guild}\n'
            e.add_field(name="Guilds", value=guild_str)
        await ctx.send(embed=e)

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
        del_guilds = ''
        exist_guilds = ''
        for g in guilds:
            if g in exist_g['guilds']:
                exist_g['guilds'].remove(g)
                del_guilds += f'{g}\n'
        db.RobBot.guilds.update_one(f, {'$set': {'guilds': exist_g['guilds']}}, upsert=True)
        await insert_transaction(ctx,'del_guild', guilds, f)
        e = discord.Embed(title='Delete Guild',
                          type='rich',
                          description=f'{member.display_name}',
                          colour=self.del_color)
        e.set_footer(text=f'executed by: {ctx.author.display_name} ')
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Deleted Guilds", value=del_guilds, inline=True)
        if not exist_g['guilds']:
            exist_guilds = 'None'
        else:
            for guild in exist_g['guilds']:
                exist_guilds += f'{guild}\n'
        e.add_field(name="Active Guilds", value=exist_guilds, inline=True)

        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Guilds(bot))
