import disnake
from dislash import *
from disnake.ext import commands
from utils import checks
from main import db
from utils.helpers import *
from utils.menu_options import *
from datetime import datetime


class GuildCommands(commands.Cog, name='Guild Commands'):
    """
  Commands for the managing Guilds
  """

    def __init__(self, bot):
        self.bot = bot
        self.add_color = disnake.Colour.green()
        self.del_color = disnake.Colour.red()
        self.info_color = disnake.Colour.orange()
        self.f = {}

    @slash_command(description="Guild Commands")
    async def guild(self, inter):
        self.f = {'member_id': str(inter.author.id), 'server_id': str(inter.guild.id)}
        pass

    @checks.is_owner()
    @guild.sub_command(description="Adds a Guild to the Server",
                       options=GUILD_ADD)
    async def add(self, inter, member, guild_name):
        f = {'owner_id': str(member.id), 'guild_name': guild_name.title(), 'current_members': []}
        # check for duplicates
        guild_entries = db.RobBot.guilds.find({'guild_name': guild_name.title()})
        async for guild in guild_entries:
            if guild_name.title() == guild['guild_name']:
                return await inter.reply("That guild already exists")
        # add to db
        await db.RobBot.guilds.insert_one({**self.f, **f})
        t = {'exec_by': str(inter.author.id), 'transaction': 'add_guild', 'data': guild_name.title(),
             'timestamp': datetime.utcnow()}
        await db.RobBot.transactions.insert_one({**t, **f})
        await member.add_roles(disnake.utils.get(inter.guild.roles, name="Guild Master"))
        # build embed
        e = disnake.Embed(title='Add a Guild',
                          type='rich',
                          description=f'',
                          colour=self.add_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=inter.author.avatar_url)
        e.add_field(name=guild_name.title(), value="Added to the Server")
        return await inter.reply(embed=e)

    @checks.is_dm()
    @guild.sub_command(description="Add a member to an existing Guild",
                       options=[
                           Option("member", "What member are you adding to a guild?",
                                  OptionType.USER, required=True)
                       ])
    async def add_member(self, inter, member):
        # load guilds and characters attached to the member you are trying to add
        guild_list = db.RobBot.guilds.find()
        char_list = db.RobBot.characters.find({"member_id": str(member.id)})
# TODO: add a check for duplicate characters so one doesnt get added twice to a guild
        # build the menus
        guilds_menu = SelectMenu(custom_id="guild_list", placeholder="Guilds", max_values=1)
        async for guild in guild_list:
            guilds_menu.add_option(label=guild["guild_name"], value=guild["guild_name"].lower())
        chars_menu = SelectMenu(custom_id="char_list", placeholder="Characters", max_values=1)
        async for char in char_list:
            chars_menu.add_option(label=char["name"], value=char["name"].lower())
        # send the drop downs
        guild_msg = await inter.reply("Which Guild?", components=[guilds_menu])
        guild_inter = await guild_msg.wait_for_dropdown()
        selected_guild = await db.RobBot.guilds.find_one({"guild_name": guild_inter.select_menu.selected_options[0].label})

        char_msg = await inter.reply("Which playable Character?", components=[chars_menu])
        char_inter = await char_msg.wait_for_dropdown()
        selected_char = await db.RobBot.characters.find_one({"member_id":str(member.id), "name": char_inter.select_menu.selected_options[0].label})


        # add entries into both guilds and members

        # add member to guilds
        selected_guild["current_members"].append(char_inter.select_menu.selected_options[0].label)
        db.RobBot.guilds.update_one({"guild_name": guild_inter.select_menu.selected_options[0].label}, {"$set": selected_guild}, upsert=True)
        # add guilds to character
        selected_char["guilds"].append(guild_inter.select_menu.selected_options[0].label)
        db.RobBot.characters.update_one({"member_id": str(member.id), "name": char_inter.select_menu.selected_options[0].label}, {"$set": selected_char}, upsert=True)
        await guild_msg.delete()
        await char_msg.delete()
        # build embed
        e = disnake.Embed(title=guild_inter.select_menu.selected_options[0].label,
                          type='rich',
                          description="",
                          colour=self.add_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=inter.author.avatar_url)
        e.add_field(name=char_inter.select_menu.selected_options[0].label, value="Added to the Guild")
        return await inter.reply(embed=e)


    @guild.sub_command(description="Views the information on a Guild", options=[
                       Option("guild_name", "What Guild?", OptionType.STRING, required=True)])
    async def view(self, inter, guild_name):
        # fuzzy search the guild
        selected_guild = None
        guilds_list = db.RobBot.guilds.find()
        async for guild in guilds_list:
            if guild_name.lower() in guild["guild_name"].lower():
                selected_guild = guild
        if not selected_guild:
            return await inter.reply("No guilds found")
        # embed
        e = disnake.Embed(title=selected_guild["guild_name"],
                          type='rich',
                          description=f'',
                          colour=self.info_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=inter.author.avatar_url)
        member_list = ''
        for m in selected_guild["current_members"]:
            member_list += f'{m}\n'
        e.add_field(name="Members", value=member_list)
        return await inter.reply(embed=e)

def setup(bot):
    bot.add_cog(GuildCommands(bot))
