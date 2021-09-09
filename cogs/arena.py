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
    @arena.sub_command(description="Adds a Fight Record",
                       options=[Option("member", "Who is the Member? (The owner of the character)", OptionType.USER, required=True)])
    async def fight(self, inter, member):
        #vars
        f = {'member_id':str(member.id), 'server_id':str(inter.guild.id)}
        char_count = await db.RobBot.characters.count_documents(f)
        char_entries = db.RobBot.characters.find(f)
        char_row = ActionRow()
        if char_count == 0:
            return await inter.reply("That Member does not have Characters set up. run `/character add`")
        async for char in char_entries:
            char_row.add_button(style=ButtonStyle.green, label=char["name"], custom_id=char["imageurl"])
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
                    e.set_thumbnail(url=char_inter.component.custom_id)
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
            char_row.add_button(style=ButtonStyle.green, label=char["name"], custom_id=char["imageurl"])
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
            e.set_thumbnail(url=char_inter.component.custom_id)
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



        # check for which pc

    #     await ctx.message.delete()
    #     if outcome not in ['w', 'l', 'W', 'L']:
    #         await ctx.send("You must provide a W for win or L for lost")
    #     else:
    #         outcome = 'win' if outcome.lower() == 'w' else 'loss'
    #     member = m_search(ctx, member)
    #     f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
    #     fi = {'beast': beast, 'outcome': outcome}
    #     fight = {**f, **fi}
    #     await db.RobBot.arena.insert_one(fight)
    #     await insert_transaction(ctx, 'fight_beast', (beast, outcome), f)
    #     e = discord.Embed(title='Arena Fight',
    #                       type='rich',
    #                       description=f'Executed by {ctx.author.display_name}',
    #                       colour=self.add_color if outcome == 'win' else self.del_color)
    #     e.set_footer(text=f'for {member.display_name}')
    #     e.set_thumbnail(url=member.avatar_url)
    #     e.add_field(name=beast.title(), value=f'Resulted in a {outcome}')
    #     await ctx.send(embed=e, delete_after=90)
    #
    # @checks.is_dm()
    # @commands.command(name='fight_record')
    # async def fight_record(self, ctx, member):
    #     """
    #     Usage: fight_record [member]
    #     """
    #     await ctx.message.delete()
    #     member = m_search(ctx, member)
    #     f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
    #     fights = db.RobBot.arena.find(f)
    #     e = discord.Embed(title='Arena Fight Record',
    #                       type='rich',
    #                       description=f'{member.display_name}',
    #                       colour=self.info_color)
    #     e.set_footer(text=f'executed by: {ctx.author.display_name} ')
    #     e.set_thumbnail(url=member.avatar_url)
    #     for fight in await fights.to_list(length=10):
    #         e.add_field(name=fight["_id"].generation_time.date(), value=f'{fight["beast"]} - *{fight["outcome"].title()}*')
    #     await ctx.send(embed=e, delete_after=90)
    #
    # @checks.is_dm()
    # @commands.command(name='arena')
    # async def arena_workflow(self, ctx):
    #     """
    #     Workflow for Arena Beasts
    #     """
    #     def workflow_m_check(m):
    #         if m.author.id == ctx.author.id:
    #             return True
    #
    #     await ctx.message.delete()
    #     # get a valid member
    #     await ctx.send("Who got in a fight?")
    #     fmember = await client.wait_for('message', check=workflow_m_check, timeout=30)
    #     member = m_search(ctx, fmember.content)
    #     # get the beast
    #     await ctx.send("What beast?")
    #     beast = await client.wait_for('message', check=workflow_m_check, timeout=30)
    #     #get the outcome
    #     await ctx.send(f'Did {member.display_name} `win` or `loss`?')
    #     outcome = await client.wait_for('message', check=workflow_m_check, timeout=30)
    #     #build the database entry
    #     f = {'member_id': str(member.id), 'server_id': str(ctx.guild.id)}
    #     fi = {'beast': beast.content, 'outcome': outcome.content}
    #     fight = {**f, **fi}
    #     await db.RobBot.arena.insert_one(fight)
    #     await insert_transaction(ctx, 'fight_beast', (beast.content, outcome.content), f)
    #     e = discord.Embed(title='Arena Fight',
    #                       type='rich',
    #                       description=f'{member.display_name}',
    #                       colour=self.add_color)
    #     e.set_footer(text=f'exec by: {ctx.author.display_name} ')
    #     e.set_thumbnail(url=member.avatar_url)
    #     e.add_field(name=beast.content.title(), value=f'Resulted in a {outcome.content.title()}')
    #
    #     await beast.delete()
    #     await fmember.delete()
    #     await outcome.delete()
    #
    #     await ctx.send(embed=e, delete_after=90)




def setup(bot):
    bot.add_cog(ArenaCommands(bot))
