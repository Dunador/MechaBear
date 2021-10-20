import disnake
from disnake.ext import commands
from disnake import Option, OptionType, OptionChoice, Embed
from utils import checks
from utils.dmClasses import DmQuest


# from utils.classes import DmQuest


class DmCommands(commands.Cog, name='DM Commands'):

    def __init__(self, bot):
        self.bot = bot

    @checks.is_dm()
    @commands.slash_command(description="DM Commands")
    async def dm(self, inter):
        pass

    @dm.sub_command(name="new_quest", description="Starts a new quest",
                    options=[Option(name="name",
                                    description="The name of the quest, will also be used as the channel names",
                                    type=OptionType.string, required=True)])
    async def dm_new_quest(self, ctx, name):
        # make an object
        quest = DmQuest(ctx, name)
        # create channels
        await quest.create_channels(ctx)
        # save to db
        quest.save(ctx)
        # return embed
        return await ctx.response.send_message(f'New quest Created {quest.rp_channel.mention}\n '
                                               f'Add players `/dm add_player {quest.name} @player`')

    @dm.sub_command(name="finish_quest", description="Closes out a quest",
                    options=[Option("name", "The name of the quest",
                                    type=OptionType.string, required=True),
                             Option("description", "A synopsis of the quest", type=OptionType.string, required=True)])
    async def dm_finish_quest(self, ctx, name, description):
        # instantiate a quest object
        await ctx.response.defer()
        quest = DmQuest(ctx, name)
        # load it from db
        await quest.load(ctx)
        # close it out
        await quest.complete(ctx, description)
        # sve to db
        quest.save(ctx)
        return await ctx.edit_original_message(content=f'Quest: `{quest.name}` completed and added to DB.')

    @dm.sub_command(name="add_member", description="Tag all members you wish to add",
                    options=[Option("quest", "part of the name of your quest",
                                    type=OptionType.string, required=True),
                             Option("member", "The member you are adding",
                                    type=OptionType.user, required=True)])
    async def add_player(self, ctx, quest, member: disnake.Member):
        # await ctx.response.defer()
        # instantiate a quest object
        quest = DmQuest(ctx, quest)
        # load it from db
        await quest.load(ctx)
        # add members
        await quest.add_player(ctx, member)
        # save to db
        quest.save(ctx)
        return await ctx.response.send_message(f'You added `{member.display_name}` to the `{quest.name}` quest')

    @dm.sub_command(name="quest_list", description="List all your quests",
                    options=[Option("status", "Active, Completed, All ?",
                                    type=OptionType.string, required=True,
                                    choices=[OptionChoice("Active", "Active"),
                                             OptionChoice("Complete", "Complete"),
                                             OptionChoice("All", "All")])])
    async def list_quests(self, ctx, status):
        # TODO: make this paginated
        await ctx.response.defer()
        e = Embed(title="List of Quests", description=f'List of quests with DM: `{ctx.author.name}`')
        e. set_thumbnail(ctx.author.display_avatar.url)

        f = {"server": str(ctx.guild.id), "dm": str(ctx.author.id)}
        if status == "Active" or status == "Complete":
            f.update({"status": status})
        quests = ctx.bot.db.dm_quests.find(f)
        async for quest in quests:
            _f = ''
            _f += f'**Synopsis**: {quest["description"]}\n'
            _f += f'**Started**: {quest["date_started"][:-7]}\n'
            _f += f'**Completed**: {quest["date_completed"][:-7]}\n'
            _f += f'**Players**: '
            for member in quest["quest_members"]:
                _m = ctx.guild.get_member(int(member))
                _f += f'{_m.name}, '
            _f = _f[:-2]
            e.add_field(name=quest['name'].title(), value=_f)
        return await ctx.edit_original_message(embeds=[e])


def setup(bot):
    bot.add_cog(DmCommands(bot))
