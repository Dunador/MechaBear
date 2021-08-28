import datetime

import discord
from discord.ext import commands
from utils import checks
from main import db
from utils.helpers import *
from datetime import datetime


class Characters(commands.Cog, name='Characters'):
    """
  Commands for the managing characters
  """

    def __init__(self, bot):
        self.bot = bot
        self.add_color = discord.Colour.green()
        self.del_color = discord.Colour.red()
        self.info_color = discord.Colour.orange()

    @commands.command(name='add_pc')
    async def add_pc(self, ctx, member, *characters):
        """
            adds a character to your list
        """
        await ctx.message.delete()
        member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        characters = list(characters)
        for pc in characters:
            db.RobBot.characters.update_one(f, {'$push': {'characters': (pc.title(), 'alive')}}, upsert=True)
        await insert_transaction(ctx, 'add_pc', characters, f)
        e = discord.Embed(title='Add Player Character',
                          type='rich',
                          description=f'{member.display_name}',
                          colour=self.add_color)
        e.set_footer(text=f'Executed by {ctx.author.display_name}')
        e.set_thumbnail(url=member.avatar_url)
        for character in characters:
            e.add_field(name=f'{character}', value=f'Added to list')
        await ctx.send(embed=e, delete_after=90)

    @commands.command(name='list_pc')
    async def list_pc(self, ctx, member=None):
        """
            Checks PCs of a member
        """
        await ctx.message.delete()
        if not member:
            member = ctx.author
        else:
            member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        t = await db.RobBot.characters.find_one(f)
        e = discord.Embed(title='List Player Character',
                          type='rich',
                          description=f'{member.display_name}',
                          color=self.info_color)
        e.set_footer(text=f'Executed by {ctx.author.display_name}')
        e.set_thumbnail(url=member.avatar_url)
        if not t['characters']:
            e.add_field(name='None', value='No characters found.')
        else:
            for character in t['characters']:
                e.add_field(name=f'{character[0]}', value=f'*{character[1].title()}*')
        await ctx.send(embed=e, delete_after=90)

    @commands.command(name='del_pc')
    async def del_pc(self, ctx, member, *characters):
        """
            deletes a character to your list
        """
        await ctx.message.delete()
        member = m_search(ctx, member)
        c_to_del = list(characters)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        exist_pc = await db.RobBot.characters.find_one(f)
        print(exist_pc)
        for c in c_to_del:
            for pc_pair in exist_pc['characters']:
                for pc in pc_pair:
                    if c in pc:
                        exist_pc['characters'].pop(exist_pc['characters'].index(pc_pair))
        db.RobBot.characters.update_one(f, {'$set': {'characters': exist_pc['characters']}}, upsert=True)
        await insert_transaction(ctx,'del_pc', characters, f)
        e = discord.Embed(title='Delete Player Character',
                          type='rich',
                          description=f'for {member.display_name}',
                          color=self.del_color)
        e.set_footer(text=f'Executed by {ctx.author.display_name}')
        e.set_thumbnail(url=member.avatar_url)
        for character in characters:
            e.add_field(name=f'{character}', value=f'Removed from list')
        await ctx.send(embed=e, delete_after=90)

    @commands.command(name='kill_pc')
    async def kill_pc(self, ctx, member, character):
        """
            kills a single character from your list
        """
        await ctx.message.delete()
        member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        c = [character, 'alive']
        char_list = await db.RobBot.characters.find_one(f)
        char_list['characters'].remove(c)
        c[1] = 'dead'
        char_list['characters'].append(c)
        db.RobBot.characters.update_one(f, {'$set': {'characters': char_list['characters']}})
        await insert_transaction(ctx, 'kill_pc', character, f)
        e = discord.Embed(title='Kill Player Character',
                          type='rich',
                          description=f'for {member.display_name}',
                          color=self.del_color)
        e.set_footer(text=f'Executed by {ctx.author.display_name}')
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name=f'{character}', value=f'was Killed in Action')
        await ctx.send(embed=e, delete_after=90)


def setup(bot):
    bot.add_cog(Characters(bot))
