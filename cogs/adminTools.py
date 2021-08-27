import asyncio
import json

import discord
from discord.ext import commands
import utils.checks as checks
from main import db, bot as client
from utils.pipelines import profile_pipeline, mod_pipeline
from utils.helpers import *

class OwnerCommands(commands.Cog, name='DM Commands'):
    """
  Commands for the owner of the Bot
  """

    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command(name='server', aliases=[])
    async def server(self, ctx):
        """
        displays what guild you in
        """
        await ctx.send(ctx.guild.id)

    @checks.is_admin()
    @commands.command(name='profile', aliases=[])
    async def profile(self, ctx, member=None):
        """
        displays full profile
        """
        await ctx.message.delete()
        if member is None:
            member = ctx.author
        else:
            member = m_search(ctx, member)
        returnstr = f'{member.display_name}\n'
        p = mod_pipeline(member.id, ctx.guild.id)
        async for operation in db.RobBot.names.aggregate(p):
            print(operation)
            for key, value in operation.items():
                returnstr += f'{key}: {value} \n'
        await ctx.send(returnstr)

    @checks.is_owner()
    @commands.command(name='dbsetup', aliases=['dbs'])
    async def dbsetup(self, ctx):
        """
        Creates the initial db of the server.
        """
        await ctx.message.delete()
        all_members = ctx.guild.members

        for member in all_members:
            f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
            if not member.bot:
                db.RobBot.names.update_one(f, {'$set': {'names': member.display_name}}, upsert=True)
                db.RobBot.tokens.update_one(f, {'$set': {'tokens': 0}}, upsert=True)
                db.RobBot.points.update_one(f, {'$set': {'points': 0}}, upsert=True)
                db.RobBot.MainQuest.update_one(f, {'$set': {'MainQuest': 0}}, upsert=True)
                db.RobBot.characters.update_one(f, {'$set': {'characters': []}}, upsert=True)
                db.RobBot.guilds.update_one(f, {'$set': {'guilds': []}}, upsert=True)
                db.RobBot.trophies.update_one(f, {'$set': {'trophies': {
                    'platinum': 0, 'gold': 0, 'silver': 0, 'copper': 0}
                }}, upsert=True)
        await ctx.send("Created All Member Keys for this Server")

    @client.event
    async def on_member_join(self, member):
        if not member.bot:
            db.RobBot.names.update_one(f, {'$set': {'names': member.display_name}}, upsert=True)
            db.RobBot.tokens.update_one(f, {'$set': {'tokens': 0}}, upsert=True)
            db.RobBot.points.update_one(f, {'$set': {'points': 0}}, upsert=True)
            db.RobBot.MainQuest.update_one(f, {'$set': {'MainQuest': 0}}, upsert=True)
            db.RobBot.characters.update_one(f, {'$set': {'characters': []}}, upsert=True)
            db.RobBot.guilds.update_one(f, {'$set': {'guilds': []}}, upsert=True)
            db.RobBot.trophies.update_one(f, {'$set': {'trophies': {
                'platinum': 0, 'gold': 0, 'silver': 0, 'copper': 0}
            }}, upsert=True)
        print(f'created new entry for {member.display_name}')


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
