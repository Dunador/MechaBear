import discord
from discord.ext import commands
import utils.checks as bot_checks
from dislash import slash_command,user_command, ContextMenuInteraction
from main import db
from datetime import datetime


class OwnerCommands(commands.Cog, name='Owner'):
    """
  Commands for the owner of the Guild
  """

    def __init__(self, bot):
        self.bot = bot
        self.add_color = discord.Colour.green()
        self.del_color = discord.Colour.red()
        self.info_color = discord.Colour.orange()
        self.f = {}

    @bot_checks.is_owner()
    @slash_command(description="Owner Commands")
    async def owner(self, inter):
        self.f = {'member_id': str(inter.author.id), 'server_id': str(inter.guild.id)}
        pass

    @user_command(name="Give Token")
    async def give_token(self, inter: ContextMenuInteraction):
        f = {'member_id': str(inter.user.id), 'server_id': str(inter.guild.id)}
        member = await db.RobBot.members.find_one(f)
        # db actions
        db.RobBot.members.update_one(f, {"$inc": {"tokens": 1}})
        t = {'exec_by': str(inter.author.id), 'transaction': 'give_token', 'data': 1, 'timestamp': datetime.utcnow()}
        await db.RobBot.transactions.insert_one({**t, **f})
        # Build Embed
        e = discord.Embed(title='Give Token',
                          type='rich',
                          description=f'{inter.author.display_name}',
                          colour=self.add_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=inter.user.avatar_url)
        e.add_field(name="Received Token", value=f'From `{inter.author.display_name}`\n'
                                                 f'`{member["tokens"]}` -> `{member["tokens"] + 1}`')
        # Responses
        await inter.respond(embed=e)

    # @bot_checks.is_owner()
    # @commands.command(name='roles', aliases=[], hidden=True)
    # async def server(self, ctx):
    #     """
    #
    #     """
    #     await ctx.send(ctx.guild.id)

    # @bot_checks.is_admin()
    # @commands.command(name='profile')
    # async def profile(self, ctx, member=None):
    #     """
    #     Displays a Members profile.
    #     """
    #     await ctx.message.delete()
    #     if member is None:
    #         member = ctx.author
    #     else:
    #         member = m_search(ctx, member)
    #     p = mod_pipeline(member.id, ctx.guild.id)
    #     e = discord.Embed(title='Profile Viewer',
    #                       type='rich',
    #                       description=f'Viewing profile for {member.name}')
    #     e.set_footer(text=f'{member.display_name}')
    #     e.set_thumbnail(url=member.avatar_url)
    #
    #     async for operation in db.RobBot.names.aggregate(p):
    #         for key, value in operation.items():
    #             value_str = ''
    #             if not value:
    #                 value_str += "None"
    #             elif value is not str:
    #                 for x in value:
    #                     value_str += f'{x}\n'
    #             else:
    #                 value_str += value
    #             e.add_field(name=f'{key.title()}',
    #                         value=value_str,
    #                         inline=True)
    #
    #     await ctx.send(embed=e)

    @bot_checks.is_owner()
    @commands.command(name="dbsetup", hidden=True)
    async def dbsetup(self, ctx):
        """
        Creates the initial db of the server.
        """
        await ctx.message.delete()
        all_members = ctx.guild.members
        # member info

        for member in all_members:
            if not member.bot:
                _mem = {"name": str(member.display_name),
                        "trophies": {"platinum": 0, "gold": 0, "silver": 0, "copper": 0},
                        "tokens": 0}
                _meta = {
                    "charapproval": True if "NEED Character Approval" not in [x.name for x in member.roles] else False,
                    "rolesselected": True if "NEED Roles Selected" not in [x.name for x in member.roles] else False,
                    "vsheetapproval": True if "NEED VSheet Approval" not in [x.name for x in member.roles] else False,
                    "memberinfo": True if "NEED Member Information" not in [x.name for x in member.roles] else False}
                f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
                await db.RobBot.members.insert_one({**f, **_mem})
                await db.RobBot.meta.insert_one({**f, **_meta})

        await ctx.send("Created All Member Keys for this Server")

    # @client.event
    # async def on_member_join(member):
    #     f = {'member_id': str(member.id), 'server_id': str(member.guild.id)}
    #     if not member.bot:
    #         db.RobBot.names.update_one(f, {'$set': {'names': member.display_name}}, upsert=True)
    #         db.RobBot.tokens.update_one(f, {'$set': {'tokens': 0}}, upsert=True)
    #         db.RobBot.points.update_one(f, {'$set': {'points': 0}}, upsert=True)
    #         db.RobBot.MainQuest.update_one(f, {'$set': {'MainQuest': 0}}, upsert=True)
    #         db.RobBot.characters.update_one(f, {'$set': {'characters': []}}, upsert=True)
    #         db.RobBot.guilds.update_one(f, {'$set': {'guilds': []}}, upsert=True)
    #         db.RobBot.trophies.update_one(f, {'$set': {'trophies': {
    #             'platinum': 0, 'gold': 0, 'silver': 0, 'copper': 0}
    #         }}, upsert=True)
    #     print(f'created new entry for {member.display_name}')


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
