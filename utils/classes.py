from discord import Member, Permissions, PermissionOverwrite
from discord.ext.commands import Context
from main import db


class ServerMember(object):

    @classmethod
    async def load(cls, ctx: Context, member: Member):
        self = ServerMember()
        self.member_id = str(member.id)
        self.server_id = str(ctx.guild.id)
        _f = {"member_id": self.member_id, "server_id": self.server_id}

        m = await db.RobBot.members.find_one(_f)
        self.name = member.display_name
        self.trophies = m["trophies"]
        self.tokens = m["tokens"]

        self.characters = []
        _c = db.RobBot.characters.find(_f)
        async for character in _c:
            c = await MemberCharacter.load(character)
            self.characters.append(c)
        return self


class MemberCharacter(object):

    @classmethod
    async def load(cls, character):
        self = MemberCharacter()
        self.member_id = character["member_id"]
        self.server_id = character["server_id"]
        _f = {"member_id": self.member_id, "server_id": self.server_id}
        self.name = character["name"]
        self.handle = character["handle"]
        self.status = character["status"]
        self.mainquest = character["mainquest"]
        self.imageurl = character["imageurl"]
        self.guilds = []
        _g = db.RobBot.guilds.find(_f)
        async for guild in _g:
            g = await CharacterGuild.load(guild)
            self.guilds.append(g)
        return self


class CharacterGuild:

    @classmethod
    async def load(cls, guild):
        self = CharacterGuild()
        self.owner_id = guild["owner_id"]
        self.server_id = guild["server_id"]
        self.name = guild["guild_name"]
        self.members = guild["current_members"]
        return self


class DmQuest:

    @classmethod
    async def create(cls, ctx: Context, quest_name):
        self = DmQuest()
        self.quest_name = " ".join(quest_name)
        self.owner = ctx.author
        self.server = ctx.guild
        self.quest_role = await self.server.create_role(name=self.quest_name, permissions=Permissions.text(),
                                                        mentionable=True,
                                                        reason=f'New Quest created by {self.owner.display_name} in MechaBear')
        self.category = await ctx.guild.create_category(name=f'🏷{self.quest_name}🏷')
        # overwrites = {self.quest_role: PermissionOverwrite(send_messages=True),
        #               self.server.default_role: PermissionOverwrite(read_messages=False)}
        # dm_overwrites = {self.server.default_role: PermissionOverwrite(read_messages=False)}
        self.rp_channel = \
            await self.category.create_text_channel(
                name=f'🎭rp-{self.quest_name}', overwrites=overwrites)
        self.ooc_channel = \
            await self.category.create_text_channel(
                name=f'🎲ooc-{self.quest_name}', overwrites=overwrites)
        self.dm_channel = \
            await self.category.create_text_channel(
                name=f'🧩dm-{self.quest_name}', overwrites=dm_overwrites)
        self.quest_members = []
        return self

    def save_quest(self):
        dm_quest = {
            "quest_owner": str(self.owner.id),
            "quest_server": str(self.server.id),
            "quest_name": self.quest_name,
            "quest_role": str(self.quest_role.id),
            "quest_category": str(self.category.id),
            "quest_members": self.quest_members
        }
        print(dm_quest)
        return
