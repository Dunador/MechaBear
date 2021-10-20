from disnake.ext import commands
from bot_config import *


def is_god():
    async def predicate(ctx):
        if str(ctx.author.id) == BOT_AUTHOR_ID:
            return True
        else:
            ctx.send("You are not the Owner of this bot, I DON\'T KNOW YOU!")

    return commands.check(predicate)


def is_owner():
    async def predicate(ctx):
        if ctx.author.id == ctx.guild.owner.id:
            return True
        else:
            ctx.send("You are not the Guild Owner, Only he has the power. ")

    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        admin_roles = ['Admin', 'Admin Tech']
        if ctx.author.id == 623277032930803742:
            return True
        for role in ctx.author.roles:
            if role.name in admin_roles:
                return True
        await ctx.send("You are not an admin")
        return False

    return commands.check(predicate)


def is_dm():
    async def predicate(ctx):
        for role in ctx.author.roles:
            if role.name == "Quest Master" or role.name == "Dungeon Master":
                return True
        else:
            await ctx.send("You are not a DM/GM")

    return commands.check(predicate)


def is_guild_master():
    async def predicate(ctx):
        for role in ctx.author.roles:
            if role.name == "Guild Master":
                return True
        else:
            await ctx.send("You are not a Guild Master")

    return commands.check(predicate)
