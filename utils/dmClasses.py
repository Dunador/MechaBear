import datetime

from disnake import Permissions, Member
from disnake.ext.commands import Context
from utils.constants import *


class DmQuest:

    def __init__(self, ctx: Context, name):
        self.name = name
        self.dm = ctx.author  # this is an object
        self.server = ctx.guild  # this is an object
        self.quest_role = None  # this is an object
        self.category = None  # this is an object
        self.rp_channel = None  # this is an object
        self.ooc_channel = None  # this is an object
        self.dm_channel = None  # this is an object
        self.quest_members = []
        self.status = "Active"
        self.date_started = datetime.datetime.utcnow()
        self.date_completed = None
        self.description = ""

    @property
    def f(self):
        return {"dm": str(self.dm.id), "server": str(self.server.id), "status": "Active"}

    async def create_channels(self, ctx: Context):
        self.quest_role = await self.server.create_role(name=self.name, permissions=Permissions.text(),
                                                        mentionable=True,
                                                        reason=f'New Quest created by {self.dm.display_name} in '
                                                               f'MechaBear')
        await self.dm.add_roles(self.quest_role)
        perms = {ctx.guild.me: CHANNEL_ADMIN, ctx.guild.default_role: CHANNEL_READ}
        self.category = await ctx.guild.create_category(name=f'🏷{self.name}🏷')
        self.rp_channel = await self.category.create_text_channel(name=f'🎭rp-{self.name}', overwrites=perms)
        self.ooc_channel = await self.category.create_text_channel(name=f'🎲ooc-{self.name}', overwrites=perms)
        perms.update({self.quest_role: CHANNEL_READ_WRITE})
        self.dm_channel = await self.category.create_text_channel(name=f'🧩dm-{self.name}', overwrites=perms)

    async def destroy_channels(self, ctx: Context):
        channels = [self.dm_channel, self.ooc_channel, self.rp_channel, self.category]
        for channel in channels:
            _c = ctx.guild.get_channel(channel.id)
            await _c.delete()

    def save(self, ctx: Context):
        # build the dict
        dm_quest = {
            "name": self.name,
            "dm": str(self.dm.id),
            "server": str(self.server.id),
            "quest_role": str(self.quest_role.id),
            "category": str(self.category.id),
            "rp_channel": str(self.rp_channel.id),
            "ooc_channel": str(self.ooc_channel.id),
            "dm_channel": str(self.dm_channel.id),
            "quest_members": self.quest_members,
            "status": self.status,
            "date_started": self.date_started,
            "date_completed": self.date_completed,
            "description": self.description
        }
        ctx.bot.db.dm_quests.update_one(self.f, {'$set': dm_quest}, upsert=True)
        return

    async def add_player(self, ctx: Context, member: Member):
        _r = ctx.guild.get_role(self.quest_role)
        await member.add_roles(self.quest_role)
        self.quest_members.append(str(member.id))

    async def remove_roles(self):
        await self.quest_role.delete()

    async def load(self, ctx: Context):
        quests = ctx.bot.db.dm_quests.find(self.f)
        async for q in quests:
            if self.name in q['name']:
                print("match found")
                self.name = q['name']
                self.dm = ctx.guild.get_member(int(q['dm']))
                self.server = ctx.bot.get_guild(int(q['server']))
                self.quest_role = ctx.guild.get_role(int(q['quest_role']))
                self.category = ctx.guild.get_channel(int(q['category']))
                self.rp_channel = ctx.guild.get_channel(int(q['rp_channel']))
                self.ooc_channel = ctx.guild.get_channel(int(q['ooc_channel']))
                self.dm_channel = ctx.guild.get_channel(int(q['dm_channel']))
                self.quest_members = q['quest_members']
                self.status = q['status']
                self.date_started = q['date_started']
                self.date_completed = q['date_completed']
                self.description = q['description']
            else:
                return
        return

    async def complete(self, ctx, description):
        # add final description
        self.description = description
        # deactivate status
        self.status = "Complete"
        # set the date
        self.date_completed = datetime.datetime.utcnow()
        # delete roles
        await self.remove_roles()
        # destroy channels
        await self.destroy_channels(ctx)
