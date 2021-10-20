from disnake.ext import commands
from utils.helpers import *
from dislash import *
from main import db, bot as client
from datetime import datetime
from utils.menu_options import *


class Characters(commands.Cog):
    """
  Commands for the managing characters
  """

    def __init__(self, bot):
        self.bot = bot
        self.add_color = disnake.Colour.green()
        self.del_color = disnake.Colour.red()
        self.info_color = disnake.Colour.orange()
        self.f = {}

    @slash_command(description="Character Commands")
    async def characters(self, inter):
        self.f = {'member_id': str(inter.author.id), 'server_id': str(inter.guild.id)}
        pass

    @characters.sub_command(description="Add a Playable Character",
                            options= CHAR_ADD)
    async def add(self, inter, name=None, handle="", status="alive", mainquest=0, imageurl=""):
        """
        Adds a Playable Character to your profile.
        """
        # checks
        # vars
        char_doc = {"name": name.title(), "handle": f'@{handle.strip().strip("@").replace(" ", "_")}',
                    "status": status, "mainquest": mainquest, "guilds": [], "imageurl": imageurl}
        db_entries = db.RobBot.characters.find(self.f)
        # logic
        async for operation in db_entries:
            if name.title() == operation['name']:
                return await inter.reply(f'{name.title()} already exists, no duplicates please.')
        # db actions
        await db.RobBot.characters.insert_one({**self.f, **char_doc})
        t = {'exec_by': str(inter.author.id), 'transaction': 'add_pc', 'data': char_doc, 'timestamp': datetime.utcnow()}
        await db.RobBot.transactions.insert_one({**t, **self.f})
        # Build Embed
        e = disnake.Embed(title='Add Player Character',
                          type='rich',
                          description=f'{inter.author.display_name}',
                          colour=self.add_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=inter.author.avatar_url if imageurl == "" else imageurl)
        # Build Embed Fields
        e.add_field(name=f'{name.title()}', value=f'Added to list')
        # responses
        await inter.reply(embed=e)

    @characters.sub_command(description="Delete a Playable Character")
    async def delete(self, inter):
        """
        Deletes a Playable Character from your profile.
        """
        # checks
        # vars
        char_count = await db.RobBot.characters.count_documents(self.f)
        db_entries = db.RobBot.characters.find(self.f)
        menu_options = []
        # logic
        async for char in db_entries:
            menu_options.append(SelectOption(char['name'], char['name'].lower()))
        msg = await inter.reply("Which Playable Characters are you deleting?", components=[
            SelectMenu(custom_id="del_pc", placeholder="Choose wisely", max_values=char_count,
                       options=menu_options)])
        inter = await msg.wait_for_dropdown()
        pc_to_del = [option.label for option in inter.select_menu.selected_options]
        # db actions
        for pc in pc_to_del:
            d = {"name": pc}
            await db.RobBot.characters.delete_one({**self.f, **d})
        t = {'exec_by': str(inter.author.id), 'transaction': 'del_pc', 'data': pc_to_del, 'timestamp': datetime.utcnow()}
        await db.RobBot.transactions.insert_one({**t, **self.f})
        # Build Embed
        e = disnake.Embed(title='Delete Player Character',
                          type='rich',
                          description=f'{inter.author.display_name}',
                          colour=self.del_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=inter.author.avatar_url)
        # Build Embed Fields
        for pc in pc_to_del:
            e.add_field(name=f'{pc.title()}', value=f'Deleted from profile')
        # responses
        await inter.reply(embed=e)

    @characters.sub_command(description="Kills a Playable Character")
    async def kill(self, inter):
        """
        Kills a Playable Character from your profile, does not remove it.
        """
        # checks
        # vars
        char_count = await db.RobBot.characters.count_documents({**self.f, "status":"alive"})
        db_entries = db.RobBot.characters.find({**self.f, "status":"alive"})
        menu_options = []
        # logic
        if char_count == 1:
            menu_options.append((SelectOption("Nevermind", "none")))
        if char_count == 0:
            return await inter.reply("You don't have any characters `alive`!")
        async for char in db_entries:
            menu_options.append(SelectOption(char['name'], char['name'].lower()))
        msg = await inter.reply("Which Playable Characters are you killing?", components=[
            SelectMenu(custom_id="kill_pc", placeholder="Rest in Peace", max_values=char_count,
                       options=menu_options)])
        inter = await msg.wait_for_dropdown()
        pc_to_kill = [option.label for option in inter.select_menu.selected_options]
        if "Nevermind" in pc_to_kill:
            return await inter.reply("Ok. Nothing Happened.")
        # db actions
        for pc in pc_to_kill:
            d = {**self.f, "name": pc}
            db.RobBot.characters.update_one(d, {'$set': {"status": "dead"}}, upsert=True)
        t = {'exec_by': str(inter.author.id), 'transaction': 'kill_pc', 'data':pc_to_kill, 'timestamp': datetime.utcnow()}
        await db.RobBot.transactions.insert_one({**t, **self.f})
        # Build Embed
        e = disnake.Embed(title='Kill a Player Character',
                          type='rich',
                          description=f'{inter.author.display_name}',
                          colour=self.del_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=inter.author.avatar_url)
        # Build Embed Fields
        for pc in pc_to_kill:
            e.add_field(name=f'{pc.title()}', value=f'Killed. :(')
        # responses
        await inter.reply(embed=e)

    @characters.sub_command(description="Revives a Playable Character")
    async def revive(self, inter):
        """
        Revives a Playable Character from your profile, does not remove it.
        """
        # checks
        # vars
        char_count = await db.RobBot.characters.count_documents({**self.f, "status":"dead"})
        db_entries = db.RobBot.characters.find({**self.f, "status":"dead"})
        menu_options = []
        # logic
        if char_count == 0:
            return await inter.reply("You don't have any characters that are `dead`!")
        if char_count == 1:
            menu_options.append((SelectOption("Nevermind", "none")))
        async for char in db_entries:
            menu_options.append(SelectOption(char['name'], char['name'].lower()))
        msg = await inter.reply("Which Playable Characters are you reviving?", components=[
            SelectMenu(custom_id="revive_pc", placeholder="Welcome back", max_values=char_count,
                       options=menu_options)])
        inter = await msg.wait_for_dropdown()
        pc_to_kill = [option.label for option in inter.select_menu.selected_options]
        if "Nevermind" in pc_to_kill:
            return await inter.reply("Ok. Nothing Happened.")
        # db actions
        for pc in pc_to_kill:
            d = {**self.f, "name": pc}
            db.RobBot.characters.update_one(d, {'$set': {"status": "alive"}}, upsert=True)
        t = {'exec_by': str(inter.author.id), 'transaction': 'revive_pc', 'data': pc_to_kill, 'timestamp': datetime.utcnow()}
        await db.RobBot.transactions.insert_one({**t, **self.f})
        # Build Embed
        e = disnake.Embed(title='Revive a Player Character',
                          type='rich',
                          description=f'{inter.author.display_name}',
                          colour=self.add_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=inter.author.avatar_url)
        # Build Embed Fields
        for pc in pc_to_kill:
            e.add_field(name=f'{pc.title()}', value=f'Revived. :)')
        # responses
        await inter.reply(embed=e)

    @characters.sub_command(description="Views your Playable Character List")
    async def view(self, inter):
        # vars
        char_len = await db.RobBot.characters.count_documents(self.f)
        entries = db.RobBot.characters.find(self.f)
        # build embeds
        if not char_len:
            e = disnake.Embed(title='List Player Characters',
                              type='rich',
                              description=f'{inter.author.display_name}',
                              color=self.info_color)
            e.set_footer(text='MechaBear v1.0')
            e.set_thumbnail(url=inter.author.avatar_url)
            e.add_field(name='None', value='No characters found.')
        else:
            async for char in entries:
                e = disnake.Embed(title=f'{char["name"].title()}',
                                  type='rich',
                                  description=f'{inter.author.display_name}',
                                  color=self.info_color)
                e.set_footer(text='MechaBear v1.0')
                e.set_thumbnail(url=f'{char["imageurl"] if char.get("imageurl") else inter.author.avatar_url}')
                e.add_field(name='@Handle', value=char["handle"])
                e.add_field(name='Status', value=char["status"])
                e.add_field(name='Main Quest', value=char["mainquest"])
                e.add_field(name='Guilds', value=char["guilds"])
        # responses
                await inter.reply(embed=e, delete_after=90)

    @characters.sub_command(description="Peregrine Post Setup")
    async def post_setup(self, inter):
        # checks
        def workflow_m_check(m):
            if m.author.id == inter.author.id:
                return True
        # vars
        char_count = await db.RobBot.characters.count_documents(self.f)
        db_entries = db.RobBot.characters.find(self.f)
        menu_options = []
        # logic
        if not char_count:
            await inter.reply("You have no characters!")
        if char_count == 1:
            menu_options.append((SelectOption("Nevermind", "none")))
        async for char in db_entries:
            menu_options.append(SelectOption(char['name'], char['name'].lower()))
        msg = await inter.reply("Set up Peregrine Post for which character?", components=[
            SelectMenu(custom_id="post_setup", placeholder="@Peregrine-Post", max_values=1,
                       options=menu_options)])
        inter = await msg.wait_for_dropdown()
        char = [option.label for option in inter.select_menu.selected_options][0]
        await inter.reply("Enter in the handle you want. Example: `my twitter handle`")
        handle = await client.wait_for('message', check=workflow_m_check, timeout=30)
        await inter.reply("Enter in the url for your Peregrine Post image")
        imageurl = await client.wait_for('message', check=workflow_m_check, timeout=30)
        handle = f'@{handle.content.strip().strip("@").replace(" ", "_")}'

        # db actions
        f = {**self.f, "name": char}
        c = {"handle": handle, "imageurl":imageurl.content}
        await db.RobBot.characters.update_one(f, {"$set": c}, upsert=True)
        t = {'exec_by': str(inter.author.id), 'transaction': 'setup_psot', 'data': c, 'timestamp': datetime.utcnow()}
        await db.RobBot.transactions.insert_one({**t, **self.f})
        # build embeds
        e = disnake.Embed(title='Peregrine Post Setup',
                          type='rich',
                          description=f'{char}',
                          colour=self.info_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=imageurl.content)
        e.add_field(name="Handle", value=handle)
        e.add_field(name="How-To", value=f'You can now send to peregrine post Use `/peregrine`')
        await inter.reply(embed=e)


def setup(bot):
    bot.add_cog(Characters(bot))
