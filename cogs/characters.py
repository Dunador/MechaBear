from discord.ext import commands
from utils.helpers import *
from dislash import *


class Characters(commands.Cog):
    """
  Commands for the managing characters
  """

    def __init__(self, bot):
        self.bot = bot
        self.add_color = discord.Colour.green()
        self.del_color = discord.Colour.red()
        self.info_color = discord.Colour.orange()
        self.f = {}

    @slash_command(description="Character Commands")
    async def characters(self, inter):
        self.f = {'member_id': str(inter.author.id), 'server_id': str(inter.guild.id)}
        pass

    @characters.sub_command(description="Add a Playable Character",
                            options=[Option("name", "Whats their name?", OptionType.STRING, required=True)])
    async def add(self, inter, name=None):
        """
        Adds a Playable Character to your profile.
        """
        # checks
        # vars
        db_entry = await db.RobBot.characters.find_one(self.f)
        exist_pc = db_entry['characters']
        # logic
        for pc in exist_pc:
            if name.title() in pc:
                return await inter.reply(f"Sorry bud, but `{name.title()} is already in there. No duplicates allowed.")
        # db actions
        db.RobBot.characters.update_one(self.f, {'$push': {'characters': (name.title(), 'alive')}}, upsert=True)
        await insert_transaction(inter, 'add_pc', name, self.f)
        # Build Embed
        e = discord.Embed(title='Add Player Character',
                          type='rich',
                          description=f'{inter.author.display_name}',
                          colour=self.add_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=inter.author.avatar_url)
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
        db_entry = await db.RobBot.characters.find_one(self.f)
        exist_pc = db_entry['characters']
        pc_len = len(exist_pc)
        menu_options = []
        # logic
        for pc in exist_pc:
            menu_options.append(SelectOption(pc[0].title(), pc[0]))
        msg = await inter.reply("Which Playable Characters are you deleting?", components=[
            SelectMenu(custom_id="del_pc", placeholder="Choose wisely", max_values=pc_len,
                       options=menu_options)])
        inter = await msg.wait_for_dropdown()
        pc_to_del = [option.label for option in inter.select_menu.selected_options]
        for pc in pc_to_del:
            for pc_pair in exist_pc:
                for ea in pc_pair:
                    if pc in ea:
                        exist_pc.pop(exist_pc.index(pc_pair))
        # db actions
        db.RobBot.characters.update_one(self.f, {'$set': {'characters': exist_pc}}, upsert=True)
        await insert_transaction(inter, 'del_pc', pc_to_del, self.f)
        # Build Embed
        e = discord.Embed(title='Delete Player Character',
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
        db_entry = await db.RobBot.characters.find_one(self.f)
        exist_pc = db_entry['characters']
        pc_len = len(exist_pc)
        menu_options = []
        # logic
        for pc in exist_pc:
            menu_options.append(SelectOption(pc[0].title(), pc[0]))
        msg = await inter.reply("Which Playable Characters are you killing off?", components=[
            SelectMenu(custom_id="kill_pc", placeholder="Choose wisely", max_values=pc_len,
                       options=menu_options)])
        inter = await msg.wait_for_dropdown()
        pc_to_kill = [option.label for option in inter.select_menu.selected_options]
        for pc in pc_to_kill:
            for pc_pair in exist_pc:
                for ea in pc_pair:
                    if pc in ea:
                        exist_pc.pop(exist_pc.index(pc_pair))
        for pc in pc_to_kill:
            exist_pc.append([pc, 'dead'])
        # db actions
        db.RobBot.characters.update_one(self.f, {'$set': {'characters': exist_pc}}, upsert=True)
        await insert_transaction(inter, 'kill_pc', pc_to_kill, self.f)
        # Build Embed
        e = discord.Embed(title='Kill a Player Character',
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
        Revives a Playable Character from your profile
        """
        # checks
        # vars
        db_entry = await db.RobBot.characters.find_one(self.f)
        exist_pc = db_entry['characters']
        pc_len = len(exist_pc)
        menu_options = []
        # logic
        for pc in exist_pc:
            menu_options.append(SelectOption(pc[0].title(), pc[0]))
        msg = await inter.reply("Which Playable Characters are you Reviving", components=[
            SelectMenu(custom_id="kill_pc", placeholder="Bring me to LIIIIFFFEEEE", max_values=pc_len,
                       options=menu_options)])
        inter = await msg.wait_for_dropdown()
        pc_to_kill = [option.label for option in inter.select_menu.selected_options]
        for pc in pc_to_kill:
            for pc_pair in exist_pc:
                for ea in pc_pair:
                    if pc in ea:
                        exist_pc.pop(exist_pc.index(pc_pair))
        for pc in pc_to_kill:
            exist_pc.append([pc, 'alive'])
        # db actions
        db.RobBot.characters.update_one(self.f, {'$set': {'characters': exist_pc}}, upsert=True)
        await insert_transaction(inter, 'revive_pc', pc_to_kill, self.f)
        # Build Embed
        e = discord.Embed(title='Revive a Player Character',
                          type='rich',
                          description=f'{inter.author.display_name}',
                          colour=self.del_color)
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
        t = await db.RobBot.characters.find_one(self.f)
        # build embed
        e = discord.Embed(title='List Player Characters',
                          type='rich',
                          description=f'{inter.author.display_name}',
                          color=self.info_color)
        e.set_footer(text='MechaBear v1.0')
        e.set_thumbnail(url=inter.author.avatar_url)
        if not t['characters']:
            e.add_field(name='None', value='No characters found.')
        else:
            for character in t['characters']:
                e.add_field(name=f'{character[0]}', value=f'*{character[1].title()}*')
        # responses
        await inter.reply(embed=e, delete_after=90)

def setup(bot):
    bot.add_cog(Characters(bot))
