import discord
from discord.ext import commands
from utils.helpers import m_search
import utils.checks as checks


class DevCommands(commands.Cog, name='Developer', command_attrs=dict(hidden=True)):
    """These are the developer commands"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        """
        return ctx.author.id == self.bot.author_id

    @commands.command(name='reload', aliases=['rl'])
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
            await ctx.send('Reloaded all Cogs')
        if cog in extensions:
            self.bot.unload_extension(cog)  # Unloads the cog
            self.bot.load_extension(cog)  # Loads the cog
            await ctx.send(f'Reloaded the {cog[5:].title()}, master.')  # Sends a message where content='Done'
        else:
            await ctx.send('Unknown Cog')  # If the cog isn't found/loaded.

    @commands.command(name="unload", aliases=['ul'])
    async def unload(self, ctx, cog):
        """
        Unload a cog.
        """
        await ctx.message.delete()
        extensions = self.bot.extensions
        if cog not in extensions:
            await ctx.send("Cog is not loaded!")
            return
        self.bot.unload_extension(cog)
        await ctx.send(f"`{cog}` has successfully been unloaded.")

    @commands.command(name="load")
    async def load(self, ctx, cog):
        """
        Loads a cog.
        """
        await ctx.message.delete()
        try:

            self.bot.load_extension(cog)
            await ctx.send(f"`{cog}` has successfully been loaded.")

        except commands.errors.ExtensionNotFound:
            await ctx.send(f"`{cog}` does not exist!")

    @commands.command(name="listcogs", aliases=['lc'])
    async def listcogs(self, ctx):
        """
        Returns a list of all enabled commands.
        """
        await ctx.message.delete()
        base_string = "```css\n"  # Gives some styling to the list (on pc side)
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n```"
        await ctx.send(base_string)

    @commands.command(name="tembed")
    async def tembed(self, ctx):
        """
        TEST EMBEDS
        """
        test_embed = discord.Embed(title='Test Embed Title',
                                   type='rich',
                                   description='The description of the Embed')
        test_embed.set_footer(text='This is a test footer')
        test_embed.add_field(name=f'{ctx.author.display_name}',
                             value=f'You have been here since {ctx.author.joined_at}',
                             inline=True)
        test_embed.add_field(name=f'{ctx.author.id}',
                             value=f'Your top role is {ctx.author.top_role}',
                             inline=True)
        await ctx.send(embed=test_embed)

    @checks.is_admin()
    @commands.command(name='say')
    async def say(self, ctx, *msg):
        await ctx.message.delete()
        await ctx.send(' '.join(msg))


def setup(bot):
    bot.add_cog(DevCommands(bot))
