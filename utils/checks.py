from discord.ext import commands
import bot_config


def is_owner():
    async def predicate(ctx):
        if str(ctx.author.id) == bot_config.BOT_AUTHOR_ID:
            return True
        elif "Admin" in [role.name for role in ctx.author.roles]:
            return True
        else:
            ctx.send("You are not the Owner of this bot, I DONT KNOW YOU!")
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



