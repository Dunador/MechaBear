import discord
from discord.ext import commands
from utils import checks
from main import db
from utils.helpers import *
from datetime import datetime


class MemberTokens(commands.Cog, name='Tokens'):
    """
  Commands for the managing tokens
  """

    def __init__(self, bot):
        self.bot = bot
        self.add_color = discord.Colour.green()
        self.del_color = discord.Colour.red()
        self.info_color= discord.Colour.orange()

    @checks.is_admin()
    @commands.command(name='give_token')
    async def give_token(self, ctx, member, tokens: int):
        """
        Usage: give_token [member] [tokens]
        """
        await ctx.message.delete()
        member = m_search(ctx, member)
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        db.RobBot.tokens.update_one(f, {'$inc': {'tokens': tokens}}, upsert=True)
        await insert_transaction(ctx,'give_token', tokens, f)
        e = discord.Embed(title='Give Token',
                          type='rich',
                          description=f'{member.display_name}',
                          colour=self.add_color)
        e.set_footer(text=f'executed by: {ctx.author.display_name} ')
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Gained Tokens", value=str(tokens), inline=True)
        await ctx.send(embed=e)

    @commands.command(name='check_tokens')
    async def check_tokens(self, ctx, member=None):
        """
        Checks tokens of a member
        """
        await ctx.message.delete()
        if not member:
            member = ctx.author
        else:
            member = m_search(ctx, member)

        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        t = await db.RobBot.tokens.find_one(f)
        e = discord.Embed(title='Check Tokens',
                          type='rich',
                          description=f'{member.display_name}',
                          colour=self.info_color)
        e.set_footer(text=f'executed by: {ctx.author.display_name} ')
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Tokens Available", value=t['tokens'], inline=True)
        await ctx.send(embed=e)

    @commands.command(name='spend_token')
    async def spend_token(self, ctx, reason):
        """
        Usage: spend_token 1 "Swapping Class"
        """
        await ctx.message.delete()
        member = ctx.author
        f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
        db.RobBot.tokens.update_one(f, {'$inc': {'tokens': -1}}, upsert=True)
        await insert_transaction(ctx,'spend_token', reason, f)
        e = discord.Embed(title='Spend Tokens',
                          type='rich',
                          description=f'{member.display_name}',
                          colour=self.del_color)
        e.set_footer(text=f'executed by: {ctx.author.display_name} ')
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Spend Tokens", value=f'-1', inline=True)
        e.add_field(name="Reason", value=reason, inline=True)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(MemberTokens(bot))
