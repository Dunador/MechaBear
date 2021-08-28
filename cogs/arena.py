from discord.ext import commands
import utils.checks as checks
from main import db, bot as client
from utils.pipelines import profile_pipeline, mod_pipeline
from utils.helpers import *
from datetime import datetime


class ArenaCommands(commands.Cog, name='Arena Commands'):
    """
  Commands for the Arena
  """

    def __init__(self, bot):
        self.bot = bot

    @checks.is_dm()
    @commands.command(name='fight')
    async def fight_beast(self, ctx, member, beast, outcome='L'):
        """
            gives a win
        """
        await ctx.message.delete()
        if outcome not in ['w', 'l', 'W', 'L']:
            await ctx.send("You must provide a W for win or L for lost")
        member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        db.RobBot.arena.update_one(f, {'$set': {'Beast': beast, 'Outcome': outcome}}, upsert=True)
        insert_transaction(ctx, 'fight_beast', (beast, outcome), f)
        await ctx.send(
            f'{member.display_name} {"wins" if outcome.lower() == "w" else "loses"} against {beast}. It is now recorded.')

    @checks.is_dm()
    @commands.command(name='fight_record')
    async def fight_record(self, ctx, member):
        """
            checks the fight records
        """
        await ctx.message.delete()
        member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        fights = db.RobBot.arena.find(f)
        returnstr = f'Fight Record for **{member.display_name}**\n\n'
        for fight in await fights.to_list(length=10):
            returnstr += f'{fight["_id"].generation_time.date()} : {fight["Beast"]}- {"Win" if fight["Outcome"].lower() == "w" else "Loss"}\n '
        await ctx.send(returnstr)


def setup(bot):
    bot.add_cog(ArenaCommands(bot))
