import discord
from dislash import *
from discord.ext import commands
from utils import checks
from main import db
from utils.helpers import *
from datetime import datetime


class GuildCommands(commands.Cog, name='Guild Commands'):
    """
  Commands for the managing Guilds
  """

    def __init__(self, bot):
        self.bot = bot
        self.add_color = discord.Colour.green()
        self.del_color = discord.Colour.red()
        self.info_color = discord.Colour.orange()
        self.f = {}

    @slash_command(description="Guild Commands")
    async def guild(self, inter):
        self.f = {'member_id': str(inter.author.id), 'server_id': str(inter.guild.id)}
        pass

    @checks.is_dm()
    @guild.sub_command(description="Adds a Guild to the Server",
                       options=[
                           Option("member", "Who is the Guild-master (the Player who runs it)",
                                  OptionType.USER, required=True),
                           Option("name", "What is the Guild Name you are adding?", OptionType.STRING, required=True)])
    async def add(self, inter, member, name):
        f = {'owner_id': str(member.id), 'guild_name': name.title()}
        # check for duplicates
        guild_entries = db.RobBot.guilds.find({'guild_name': name.title()})
        async for guild in guild_entries:
            if name.title() == guild['guild_name']:
                return await inter.reply("That guild already exists")
        # add to db
        await db.RobBot.guilds.insert_one({**self.f, **f})
        t = {'exec_by': str(inter.author.id), 'transaction': 'add_guild', 'data': name.title(),
             'timestamp': datetime.utcnow()}
        await db.RobBot.transactions.insert_one({**t, **f})
        # build embed
        e = discord.Embed(title='Add a Guild',
                          type='rich',
                          description=f'',
                          colour=self.add_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=inter.author.avatar_url)
        e.add_field(name=name.title(), value="Added to the Server")
        return await inter.reply(embed=e)

    # @commands.command(name='add_guild')
    # async def add_guild(self, ctx, member, *guilds):
    #     """
    #     Usage: add_guild [member(required)] [guilds]
    #     """
    #     await ctx.message.delete()
    #     member = m_search(ctx, member)
    #     f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
    #     e = discord.Embed(title='Add a Guild',
    #                       type='rich',
    #                       description=f'{member.display_name}',
    #                       colour=self.add_color)
    #     e.set_footer(text=f'executed by: {ctx.author.display_name} ')
    #     e.set_thumbnail(url=member.avatar_url)
    #     guilds = list(guilds)
    #     guild_list = ''
    #     for pc in guilds:
    #         db.RobBot.guilds.update_one(f, {'$push': {'guilds': pc}}, upsert=True)
    #         guild_list += f'{pc}\n'
    #     e.add_field(name="Guild Added", value=guild_list)
    #     await insert_transaction(ctx, 'add_guild', guilds, f)
    #     await ctx.send(embed=e)
    #
    # @commands.command(name='list_guilds', aliases=['lg'])
    # async def list_guilds(self, ctx, member=None):
    #     """
    #         Checks guilds of a member
    #     """
    #     await ctx.message.delete()
    #     if not member:
    #         member = ctx.author
    #     else:
    #         member = m_search(ctx, member)
    #     f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
    #     t = await db.RobBot.guilds.find_one(f)
    #     e = discord.Embed(title='List Guilds',
    #                       type='rich',
    #                       description=f'{member.display_name}',
    #                       colour=self.info_color)
    #     e.set_footer(text=f'executed by: {ctx.author.display_name} ')
    #     e.set_thumbnail(url=member.avatar_url)
    #     guild_str = ''
    #     if not t['guilds']:
    #         e.add_field(name="Guilds", value="None")
    #     else:
    #         for guild in t['guilds']:
    #             guild_str += f'{guild}\n'
    #         e.add_field(name="Guilds", value=guild_str)
    #     await ctx.send(embed=e)
    #
    # @commands.command(name='del_guild')
    # async def del_guild(self, ctx, member, *guilds):
    #     """
    #         deletes a guild to your list
    #     """
    #     await ctx.message.delete()
    #     member = m_search(ctx, member)
    #     guilds = list(guilds)
    #     f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
    #     exist_g = await db.RobBot.guilds.find_one(f)
    #     del_guilds = ''
    #     exist_guilds = ''
    #     for g in guilds:
    #         if g in exist_g['guilds']:
    #             exist_g['guilds'].remove(g)
    #             del_guilds += f'{g}\n'
    #     db.RobBot.guilds.update_one(f, {'$set': {'guilds': exist_g['guilds']}}, upsert=True)
    #     await insert_transaction(ctx, 'del_guild', guilds, f)
    #     e = discord.Embed(title='Delete Guild',
    #                       type='rich',
    #                       description=f'{member.display_name}',
    #                       colour=self.del_color)
    #     e.set_footer(text=f'executed by: {ctx.author.display_name} ')
    #     e.set_thumbnail(url=member.avatar_url)
    #     e.add_field(name="Deleted Guilds", value=del_guilds, inline=True)
    #     if not exist_g['guilds']:
    #         exist_guilds = 'None'
    #     else:
    #         for guild in exist_g['guilds']:
    #             exist_guilds += f'{guild}\n'
    #     e.add_field(name="Active Guild s", value=exist_guilds, inline=True)
    #
    #     await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(GuildCommands(bot))
