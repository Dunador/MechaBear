from discord.ext import tasks, commands
from main import bot as client
from random import randint
from utils.menu_options import *

class BackgroundTasks(commands.Cog):

    def __init__(self, bot):
        self.index = 0
        self.im_awake.start()
        self.do_quote.start()
        self.bot = bot
        self.quotes = ICE_QUOTES
        self.channel = None
        self.guild = None

    def cog_unload(self):
        self.im_awake.cancel()

    def load_f(self):
        self.guild = client.get_guild(435645321029353472)
        self.channel = self.guild.get_channel(829174177532739644)

    @tasks.loop(hours=1)
    async def im_awake(self):
        await self.channel.send("I'm alive. I check this every hour..")

    @im_awake.before_loop
    async def before_awake(self):
        print('waiting...')
        await self.bot.wait_until_ready()
        self.load_f()

    @tasks.loop(hours=3)
    async def do_quote(self):
        await self.channel.send(self.quotes[randint(0,len(self.quotes)-1)])

    @do_quote.before_loop
    async def before_awake(self):
        await self.bot.wait_until_ready()

    # @tasks.loop(hours=24)
    # async def look_for_inactives(self):
    #    all_members = self.guild.members
    #    inactive_members = [member.mention for member in all_members while ""]

def setup(bot):
    bot.add_cog(BackgroundTasks(bot))
