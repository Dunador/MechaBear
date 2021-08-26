import asyncio
import json

import discord
from discord.ext import commands
import utils.checks as checks
from main import db
from utils.pipelines import profile_pipeline, mod_pipeline


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
    async def profile(self, ctx, member: discord.Member):
        """
        displays full profile
        """
        returnstr = ''
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        fields = ['names', 'MainQuest', 'characters', 'guilds', 'points', 'tokens', 'trophies']
        for each in fields:
            a = await db.RobBot[each].find_one(f)
            print(a)
            returnstr += f'{each}: {a} \n'
        # TODO: instances of member.id need to be stringified.
        # p = mod_pipeline(member.id, ctx.guild.id)
        # print(p)
        # async for operation in db.RobBot.names.aggregate(p):
        #     print(operation)
        #     for key, value in operation.items():
        #         returnstr += f'{key}: {value} \n'
        await ctx.send(returnstr)

    @checks.is_owner()
    @commands.command(name='dbsetup', aliases=['dbs'])
    async def dbsetup(self, ctx):
        """
    Creates the initial db of the server.
    """
        all_members = ctx.guild.members

        for member in all_members:
            f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
            if not member.bot:
                db.RobBot.names.update_one(f, {'$set': {'display_name': member.display_name}}, upsert=True)
                db.RobBot.tokens.update_one(f, {'$set': {'tokens': 0}}, upsert=True)
                db.RobBot.points.update_one(f, {'$set': {'points': 0}}, upsert=True)
                db.RobBot.MainQuest.update_one(f, {'$set': {'MainQuest': 0}}, upsert=True)
                db.RobBot.characters.update_one(f, {'$set': {'characters': []}}, upsert=True)
                db.RobBot.guilds.update_one(f, {'$set': {'guilds': []}}, upsert=True)
                db.RobBot.trophies.update_one(f, {'$set': {'trophies': {
                    'platinum': 0, 'gold': 0, 'silver': 0, 'copper': 0}
                }}, upsert=True)
        await ctx.send("Created All Member Keys for this Server")

    # @commands.command(name='listmembers', aliases=['lm'])
    # async def listmembers(self, ctx):
    #     """
    # READ ALL: Lists all Member Collections
    # """
    #     returnstr = ""
    #     allMembers = ctx.guild.members
    #     for member in allMembers:
    #         if not member.bot:
    #             my_doc = await db[f'{ctx.guild.id}'][f'{member.id}'].find_one({"id": member.id})
    #             returnstr += f'{my_doc["name"]} '
    #     await ctx.send(returnstr)
    #
    # @commands.command(name='dblist', aliases=['dbl'])
    # async def dblist(self, ctx, member: discord.Member = False):
    #     """
    # READ ALL: Lists all keys in DB created.
    # """
    #     if not member:
    #         results = db.find()
    #         returnstr = ""
    #         for document in await results.to_list(length=100):
    #             returnstr += f'{document}\n'
    #             try:
    #                 await ctx.send(returnstr)
    #             except:
    #                 await ctx.send("Empty Ass DB")
    #             finally:
    #                 pass
    #     else:
    #         amember = db[int(member.id)]
    #         await ctx.send(amember)
    #
    # @commands.command(name='dbpurge', aliases=['dbp'])
    # async def dbpurge(self, ctx):
    #     """
    # DELETE ALL: Delets all keys in DB crated.
    # """
    #     dbkeys = db.keys()
    #     for key in dbkeys:
    #         del db[key]
    #     await ctx.send("All Keys Deleted. DB Purged. I hope your are happy.")
    #
    # @commands.command(name='setPC', aliases=['spc'])
    # async def set_user_pc(self, ctx, member: discord.Member, PCName):
    #     """
    # CREATE : adds a PC to a key
    # """
    #     userdata = await db.DesterniaData.find_one({member.id})
    #     # userdata = json.loads(db[member.id])
    #     PCName = str("PC-" + PCName)
    #     userdata.update({PCName: {}})
    #     await db.DesterniaData.insert_one(userdata)
    #     # db[member.id] = json.dumps(userdata)
    #     await ctx.send(f"Added {PCName} to {member.name}")
    #
    # @commands.command(name='remPC', aliases=['rpc'])
    # async def rem_user_pc(self, ctx, member: discord.Member, PCName):
    #     """
    # DELETE : deletes a PC to a key
    # """
    #     userdata = await db.DesterniaData.find_one({member.id})
    #     # userdata = json.loads(db[member.id])
    #     PCName = str("PC-" + PCName)
    #     try:
    #         userdata.pop(PCName)
    #         await db.DesterniaData.delete_many(userdata)
    #         # db[member.id] = json.dumps(userdata)
    #     except:
    #         await ctx.send("PC Does not exists for that User. Check it with `dblist`")
    #     await ctx.send(f"Removed {PCName} from {member.name}")

    # adds key to db on member join
    # """
    # @commands.Cog.listener('on_member_join')
    # async def member_join_event(self, member):
    #     if not member.bot:
    #         db[member.id] = json.dumps("{}")
    #
    # # removes key to db on member removal
    # @commands.Cog.listener('on_member_remove')
    # async def member_leave_event(self, member):
    #     if not member.bot:
    #         db.pop(member.id)
    # """


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
