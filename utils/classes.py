from discord import Member
from discord.ext.commands import Context
from main import db

class GuildMember:

    def __init__(self,ctx: Context, member: Member):
        self.member_id = str(member.id)
        self.server_id = str(ctx.guild.id)


        self.name = member.display_name
        self.trophies = {}
        self.tokens = 0