from discord.ext import commands
import utils.checks as checks
from main import db, bot as client
from utils.pipelines import profile_pipeline, mod_pipeline
from utils.helpers import *
from datetime import datetime
from dislash import *
from pymongo import DESCENDING


class ArenaCommands(commands.Cog, name='Arena Commands'):
    """
  Commands for the Arena
  """

    def __init__(self, bot):
        self.bot = bot
        self.add_color = discord.Colour.green()
        self.del_color = discord.Colour.red()
        self.info_color = discord.Colour.orange()
        self.f = {}

    @slash_command(description='Arena Commands')
    async def arena(self, inter):
        self.f = {'member_id': str(inter.author.id), 'server_id': str(inter.guild.id)}
        pass

    @checks.is_dm()
    @arena.sub_command(description="Adds a Beast Fight Record",
                       options=[Option("member", "Who is the Member? (The owner of the character)", OptionType.USER, required=True)])
    async def fight_beast(self, inter, member):
        #vars
        f = {'member_id':str(member.id), 'server_id':str(inter.guild.id)}
        char_count = await db.RobBot.characters.count_documents(f)
        char_entries = db.RobBot.characters.find(f)
        char_row = ActionRow()
        if char_count == 0:
            return await inter.reply("That Member does not have Characters set up. run `/character add`")
        async for char in char_entries:
            char_row.add_button(style=ButtonStyle.green, label=char["name"], custom_id=char["name"].lower() )
        char_msg = await inter.reply("Which Player Character fought?", components=[char_row])
        on_click = char_msg.create_click_listener(timeout=60)
        @on_click.no_checks()
        async def chose_character(char_inter):
            f.update({"character_name": char_inter.component.label})
            await char_msg.delete()

            beast_entries = db.RobBot.beasts.find()
            beast_row = ActionRow()
            async for beast in beast_entries:
               beast_row.add_button(style=ButtonStyle.gray, label=beast["name"], custom_id=beast["name"].lower())
            beast_msg = await inter.reply("Which Beast?", components=[beast_row])
            on_click = beast_msg.create_click_listener(timeout=60)
            @on_click.no_checks()
            async def chose_beast(beast_inter):
                f.update({"beast_name": beast_inter.component.label})
                await beast_msg.delete()
                outcome_row = ActionRow()
                outcome_row.add_button(style=ButtonStyle.success, label="Win")
                outcome_row.add_button(style=ButtonStyle.danger, label="Loss")
                outcome_row.add_button(style=ButtonStyle.grey, label="Tie")
                outcome_msg = await inter.reply("Outcome?", components=[outcome_row])
                on_click = outcome_msg.create_click_listener(timeout=60)
                @on_click.no_checks()
                async def chose_outcome(outcome_inter):
                    f.update({"outcome": outcome_inter.component.label})
                    await outcome_msg.delete()
                    await db.RobBot.arena.insert_one(f)
                    t = {'exec_by': str(inter.author.id), 'transaction': 'add_fight', 'data': f,
                         'timestamp': datetime.utcnow()}
                    await db.RobBot.transactions.insert_one({**t, **f})
                    e = discord.Embed(title='Add a Fight Record',
                                      type='rich',
                                      description=f'`{f["character_name"]}` fought `{f["beast_name"]}` and resulted in a `{f["outcome"]}`',
                                      colour=self.del_color if f["outcome"] == "Loss" else self.add_color)
                    e.set_footer(text='MechaBear v1.0')
                    # e.set_thumbnail(url=char_inter.component.custom_id)
                    return await inter.reply(embed=e)

    @checks.is_dm()
    @arena.sub_command(description="Adds a PvP Fight Record",
                       options=[Option("member1", "Who is the Member? (The owner of the first character)", OptionType.USER, required=True),
                                Option("member2", "Who is the other Member? (The owner of the second character)", OptionType.USER, required=True)])
    async def fight_pvp(self, inter, member1, member2):
        #vars
        f = {'member_id':str(member1.id), 'server_id':str(inter.guild.id)}
        g = {'member_id':str(member2.id), 'server_id':str(inter.guild.id)}
        char1_count = await db.RobBot.characters.count_documents(f)
        char2_count = await db.RobBot.characters.count_documents(f)
        char1_entries = db.RobBot.characters.find(f)
        char2_entries = db.RobBot.characters.find(g)
        char1_row = ActionRow()
        char2_row = ActionRow()

        if char1_count == 0:
            return await inter.reply(f'{member1.display_name} does not have Characters set up. run `/character add`')
        async for char in char1_entries:
            char1_row.add_button(style=ButtonStyle.green, label=char["name"], custom_id=char["name"].lower())
        if char2_count == 0:
            return await inter.reply(f"{member2.display_name} does not have Characters set up. run `/character add`")
        async for char in char2_entries:
            char2_row.add_button(style=ButtonStyle.green, label=char["name"], custom_id=char["name"].lower())

        char1_msg = await inter.reply("First Player Character that fought?", components=[char1_row])
        on_click = char1_msg.create_click_listener(timeout=60)
        @on_click.no_checks()
        async def chose_character1(char1_inter):
            f.update({"character_name": char1_inter.component.label})
            await char1_msg.delete()

            char2_msg = await inter.reply("Second Player Character that fought?", components=[char2_row])
            on_click = char2_msg.create_click_listener(timeout=60)

            @on_click.no_checks()
            async def chose_character2(char2_inter):
                g.update({"character_name": char2_inter.component.label})
                await char2_msg.delete()

                outcome_row = ActionRow()
                outcome_row.add_button(style=ButtonStyle.success, label="Win")
                outcome_row.add_button(style=ButtonStyle.danger, label="Loss")
                outcome_row.add_button(style=ButtonStyle.grey, label="Tie")
                outcome_msg = await inter.reply("Outcome?", components=[outcome_row])
                on_click = outcome_msg.create_click_listener(timeout=60)
                @on_click.no_checks()
                async def chose_outcome(outcome_inter):
                    f.update({"outcome": outcome_inter.component.label, "beast_name": char2_inter.component.label})
                    g.update({"outcome": "Tie" if outcome_inter.component.label == "Tie" else "Loss" if outcome_inter.component.label == "Win" else "Win", "beast_name": char1_inter.component.label})

                    await outcome_msg.delete()
                    # add both outcomes to each character
                    # character1
                    await db.RobBot.arena.insert_one(g)
                    await db.RobBot.arena.insert_one(f)
                    t = {'exec_by': str(inter.author.id), 'transaction': 'add_pvp', 'data': [f,g],
                         'timestamp': datetime.utcnow()}
                    await db.RobBot.transactions.insert_one({**t, **f})
                    e = discord.Embed(title='Add a PvP Fight Record',
                                      type='rich',
                                      description=f'`{f["character_name"]}` fought `{g["character_name"]}` and resulted in a `{f["outcome"]}` for {f["character_name"]}',
                                      colour=self.del_color if f["outcome"] == "Loss" else self.add_color)
                    e.set_footer(text='MechaBear v1.0')
                    # e.set_thumbnail(url=char_inter.component.custom_id)
                    return await inter.reply(embed=e)


    @checks.is_dm()
    @arena.sub_command(description="Adds a Beast",
                           options=[Option("name", "Whats the name of the beast?", OptionType.STRING,
                                           required=True)])
    async def add_beast(self, inter, name):
        beast_entries = db.RobBot.beasts.find()
        existing_beasts = [beast["name"] async for beast in beast_entries]
        if name.title() in existing_beasts:
            return await inter.reply("Already exists.")
        beast = {"name":name.title()}
        # db insert
        await db.RobBot.beasts.insert_one({**self.f, **beast})
        t = {'exec_by': str(inter.author.id), 'transaction': 'add_beast', 'data': name,
             'timestamp': datetime.utcnow()}
        await db.RobBot.transactions.insert_one({**t, **self.f})
        return await inter.reply(f'{name.title()} added to the DB')

    @arena.sub_command(description="Shows a Playable Characters Fight Record",
                       options=[Option("member", "Who is the Member? (The owner of the character)", OptionType.USER,
                                       required=True)])
    async def record(self, inter, member):
        # vars
        f = {'member_id': str(member.id), 'server_id': str(inter.guild.id)}
        char_count = await db.RobBot.characters.count_documents(f)
        char_entries = db.RobBot.characters.find(f)
        char_row = ActionRow()
        if char_count == 0:
            return await inter.reply("That Member does not have Characters set up. run `/character add`")
        async for char in char_entries:
            char_row.add_button(style=ButtonStyle.green, label=char["name"], custom_id=char["name"].lower())
        char_msg = await inter.reply("Which Player Character fought?", components=[char_row])
        on_click = char_msg.create_click_listener(timeout=60)

        @on_click.no_checks()
        async def chose_character(char_inter):
            f.update({"character_name": char_inter.component.label})
            await char_msg.delete()
            fight_count = db.RobBot.arena.count_documents(f)
            if not fight_count:
                return await inter.reply("Member has no Playable Characters set up.")
            fight_list = db.RobBot.arena.find(f).sort('_id', DESCENDING)
            e = discord.Embed(title='Fight Record',
                              type='rich',
                              description=f'Viewing Fight Record for `{char_inter.component.label}`',
                              colour=self.info_color)
            e.set_footer(text='MechaBear v1.0')
            # e.set_thumbnail(url=char_inter.component.custom_id)
            async for fight in fight_list:
                e.add_field(name=f'{fight["_id"].generation_time.date()}', value=f'vs `{fight["beast_name"]}`\n\n***{fight["outcome"]}***')
            await inter.reply(embed=e)

    @arena.sub_command(description="Shows a Beast's Fight Record")
    async def beast_record(self, inter):
        # vars
        beasts = db.RobBot.beasts.find()
        beast_row = ActionRow()
        async for beast in beasts:
            beast_row.add_button(style=ButtonStyle.grey, label=f'{beast["name"]}')
        beast_msg = await inter.reply("Check Records for which Beast?", components=[beast_row])
        on_click = beast_msg.create_click_listener(timeout=60)

        @on_click.no_checks()
        async def chose_beast(beast_inter):
            await beast_msg.delete()
            fight_list = db.RobBot.arena.find({"beast_name": beast_inter.component.label}).sort('_id', DESCENDING)
            e = discord.Embed(title='Fight Record',
                              type='rich',
                              description=f'Viewing Fight Record for `{beast_inter.component.label}`',
                              colour=self.info_color)
            e.set_footer(text='MechaBear v1.0')
            e.set_thumbnail(url=inter.author.avatar_url)
            async for fight in fight_list:
                e.add_field(name=f'{fight["_id"].generation_time.date()}',
                            value=f'vs `{fight["character_name"]}`\n\n***Character {fight["outcome"]}***')
            await inter.reply(embed=e)


def setup(bot):
    bot.add_cog(ArenaCommands(bot))
