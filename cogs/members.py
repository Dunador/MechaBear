import disnake
from disnake.ext import commands
from utils.classes import ServerMember


class MemberCommands(commands.Cog, name='Member Commands'):
    """
    User Commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='member')
    async def member(self, ctx, member: disnake.Member):
        """
        Testing the Classes
        """
        returnstr = ''
        this_guy = await ServerMember.load(ctx, member)
        returnstr += f'**Trophies**: {this_guy.trophies}\n' \
                     f'**Tokens**: {this_guy.tokens}'
        e = disnake.Embed(description=returnstr)
        e.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        e.title = "Desternia Member Profile"
        e.set_thumbnail(url=ctx.author.avatar_url)
        e.set_footer(text="MechaBear")
        await ctx.send(embed=e)
        pass


def setup(bot):
    bot.add_cog(MemberCommands(bot))
