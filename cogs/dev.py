import disnake
from disnake.ext import commands
from utils import checks


class DevCommands(commands.Cog, name='Developer', command_attrs=dict(hidden=True)):
    """These are the developer commands"""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_god()
    @commands.command(name="load")
    async def load(self, ctx, cog):
        """
        Loads a cog.
        """
        await ctx.message.delete()
        cog = f'cogs.{cog}'
        try:
            self.bot.load_extension(cog)
            await ctx.send(f"`{cog}` has successfully been loaded.")
        except commands.errors.ExtensionNotFound:
            await ctx.send(f"`{cog}` does not exist!")

    @checks.is_god()
    @commands.command(name='reload')
    async def reload(self, ctx, cog):
        """
        Reloads a cog.
        """
        await ctx.message.delete()
        extensions = self.bot.extensions
        if cog == 'all':
            for extension in extensions:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            return await ctx.send('Reloaded all Cogs')
        cog = f'cogs.{cog}'
        if cog in extensions:
            self.bot.unload_extension(cog)  # Unloads the cog
            self.bot.load_extension(cog)  # Loads the cog
            await ctx.send(f'Reloaded the {cog} cog, master.')  # Sends a message where content='Done'
        else:
            await ctx.send('Unknown Cog')  # If the cog isn't found/loaded.

    @checks.is_god()
    @commands.command(name="unload")
    async def unload(self, ctx, cog):
        """
        Unload a cog.
        """
        await ctx.message.delete()
        cog = f'cogs.{cog}'
        extensions = self.bot.extensions
        if cog not in extensions:
            await ctx.send("Cog is not loaded!")
            return
        self.bot.unload_extension(cog)
        await ctx.send(f"`{cog}` has successfully been unloaded, Master.")

    @commands.slash_command(description="Responds with 'World'")
    async def hello(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("World")


def setup(bot):
    bot.add_cog(DevCommands(bot))
