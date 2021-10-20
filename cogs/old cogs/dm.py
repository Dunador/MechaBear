from discord.ext import commands
from utils.classes import DmQuest


class DmCommands(commands.Cog, name='DM Commands'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="new_quest")
    async def dm_new_quest(self, ctx, *quest_name):
        quest = await DmQuest.create(ctx, quest_name)
        quest.save_quest()
        return await ctx.send(f'Quest Name > `{quest.quest_name}`\n'
                              f'Category > `{quest.category.name}`\n'
                              f'RP Channel > `{quest.rp_channel.name}`\n'
                              f'OOC Channel > `{quest.ooc_channel.name}`\n'
                              f'DM Channel > `{quest.dm_channel.name}`\n')

    @commands.command(name="tt")
    async def tt(self, ctx):
        this_chan = ctx.author.guild.get_channel(887902396192292924)
        chan_ovr = this_chan.overwrites
        # for role, ovr in chan_ovr.items():
#             print(ovr.pair()) #TODO
# (<Permissions value=0>, <Permissions value=1024>)
# (<Permissions value=1024>, <Permissions value=0>)
# (<Permissions value=536871952>, <Permissions value=0>)
# (<Permissions value=2048>, <Permissions value=1024>)
# @everyone
# MrRobinhood5#1999
# SystemBots
# test quest
        return

def setup(bot):
    bot.add_cog(DmCommands(bot))
