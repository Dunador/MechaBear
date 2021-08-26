import discord
from discord.ext import commands
from utils import checks
from main import db


class Characters(commands.Cog, name='Characters'):
    """
  Commands for the managing characters
  """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add_pc')
    async def add_pc(self, ctx, member: discord.Member, *characters):
        """
            adds a character to your list
        """
        f = {'member_id': member.id, 'server_id': ctx.guild.id}
        characters = list(characters)

        for pc in characters:
            db.RobBot.characters.update_one(f, {'$push': {'characters': pc}}, upsert=True)
        await ctx.send(f'{ctx.author.display_name} adds {characters} to their list')

    @commands.command(name='list_pc')
    async def list_pc(self, ctx, member: discord.Member = None):
        """
            Checks PCs of a member
        """
        if not member:
            member = ctx.author
        f = {'member_id': member.id, 'server_id': ctx.guild.id}
        t = await db.RobBot.characters.find_one(f)
        await ctx.send(f'{member.display_name} has {t["characters"]} as characters')

    @commands.command(name='del_pc')
    async def del_pc(self, ctx, member: discord.Member, *characters):
        """
            deletes a character to your list
        """
        characters = list(characters)
        f = {'member_id': member.id, 'server_id': ctx.guild.id}
        exist_pc = await db.RobBot.characters.find_one(f)
        for pc in characters:
            if pc in exist_pc['characters']:
                exist_pc['characters'].remove(pc)
        db.RobBot.characters.update_one(f, {'$set': {'characters': exist_pc['characters']}}, upsert=True)
        await ctx.send(f'{ctx.author.display_name} modifies their characters to {exist_pc["characters"]}')


def setup(bot):
    bot.add_cog(Characters(bot))
