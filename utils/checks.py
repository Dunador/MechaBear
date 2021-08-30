from discord.ext import commands


def is_owner():
    async def predicate(ctx):
        author_id = ctx.bot.author_id
        if ctx.author.id == author_id:
            return True
        else:
            await ctx.send("Only the Bot owner can do this.")

    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        admin_roles = ['Admin', 'Admin Tech']
        if ctx.author.id == 623277032930803742:
            return True
        for role in ctx.author.roles:
            if role.name in admin_roles:
                return True
        else:
            await ctx.send("You are not an admin")

    return commands.check(predicate)


def is_dm():
    async def predicate(ctx):
        for role in ctx.author.roles:
            if role.name == "Quest Master" or role.name == "Dungeon Master":
                return True
        else:
            await ctx.send("You are not a DM/GM")
    return commands.check(predicate)
