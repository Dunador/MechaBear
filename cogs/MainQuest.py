import discord
from discord.ext import commands
from utils import checks
from main import db
from utils.helpers import *
from datetime import datetime


class MainQuest(commands.Cog, name='Main Quest'):
    """
  Commands for the managing MainQuest Stuff
  """

    def __init__(self, bot):
        self.bot = bot
        self.add_color = discord.Colour.green()
        self.del_color = discord.Colour.red()
        self.info_color= discord.Colour.orange()

    @checks.is_dm()
    @commands.command(name='do_quest')
    async def complete_quest(self, ctx, member, quest: int = 1):
        """
        Usage: do_quest [member]
        """
        await ctx.message.delete()
        member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        db.RobBot.MainQuest.update_one(f, {'$inc': {'MainQuest': quest}}, upsert=True)
        await insert_transaction(ctx,'complete_quest', quest, f)
        e = discord.Embed(title='Complete Main Quest',
                          type='rich',
                          description=f'{member.display_name}',
                          colour=self.info_color)
        e.set_footer(text=f'executed by: {ctx.author.display_name} ')
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Main Quest", value=str(quest))
        await ctx.send(embed=e)

    @commands.command(name='check_quest')
    async def m_quest(self, ctx, member=None):
        """
            Checks Main Quest of a member
            Optional: part of the member name, leave blank for yourself
            Example: check_quest rob
        """
        await ctx.message.delete()
        if not member:
            member = ctx.author
        else:
            member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        t = await db.RobBot.MainQuest.find_one(f)
        e = discord.Embed(title='Main Quest',
                          type='rich',
                          description=f'{member.display_name}',
                          colour=self.info_color)
        e.set_footer(text=f'executed by: {ctx.author.display_name} ')
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Current Main Quest", value=str(t["MainQuest"]))
        await ctx.send(embed=e)

    # @checks.is_admin()
    # @commands.command(name='remove_quest')
    # async def remove_quest(self, ctx, member, quest: int):
    #     """
    #         Takes Main Quest  to a Member
    #     """
    #     await ctx.message.delete()
    #     member = m_search(ctx, member)
    #     f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
    #     db.RobBot.MainQuest.update_one(f, {'$dec': {'MainQuest': quest}}, upsert=True)
    #     await insert_transaction(ctx,'remove_quest', quest, f)
    #     await ctx.send(f'{member.display_name} Loses {quest} Main Quest')


def setup(bot):
    bot.add_cog(MainQuest(bot))
