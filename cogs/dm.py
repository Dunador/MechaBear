from discord.ext import commands
from utils.classes import DmQuest


class DmCommands(commands.Cog, name='DM Commands'):

    def __init(self, bot):
        self.bot = bot

    @commands.command(name="new_quest")
    async def dm_new_quest(self, ctx, *quest_name):

        quest = await DmQuest.create(ctx, quest_name)

        return await ctx.send(f'Quest Name > {quest.quest_name}'
                              f'Category > {quest.category_name}\n'
                              f'RP Channel > {quest.rp_channel_name}\n'
                              f'OOC Channel > {quest.ooc_channel_name}\n'
                              f'DM Channel > {quest.dm_channel_name}\n')


def setup(bot):
    bot.add_cog(DmCommands(bot))
