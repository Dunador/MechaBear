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
        if ctx.author.permissions_in(ctx.channel).administrator or ctx.author.id == ctx.bot.author_id:
            return True
        else:
            await ctx.send("You are not an admin")
    return commands.check(predicate)
