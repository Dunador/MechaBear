from discord.ext import commands
import utils.checks as checks
from main import db, bot as client
from utils.pipelines import profile_pipeline, mod_pipeline
from utils.helpers import *
from datetime import datetime
from dislash import *

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

    @slash_command(Description='Arena Commands')
    async def arena(self, inter):
        self.f = {'member_id': str(inter.author.id), 'server_id': str(inter.guild.id)}
        pass

    @arena.sub_command(description="Adds a Fight Record",
                       options=[Option("member", "Who is the Member? (The owner of the character)", OptionType.USER, required=True)])
    async def fight(self, inter, member):
        #vars
        f = {'member_id':str(member.id), 'guild_id':str(inter.guild.id)}
        char_entries = db.RobBot.characters.find(f)
        beast_entries = db.RobBot.beasts.find()
        char_row = ActionRow()
        beast_row = ActionRow()
        async for char in char_entries:
            char_row.add_button(style=ButtonStyle.green, label=char["name"], custom_id=char["name"].lower())
        async for beast in beast_entries:
            beast_row.add_button(style=ButtonStyle.gray, label=beast["name"], custom_id=beast["name"].lower())
        char_msg = await inter.reply("Which Player Character fought?", components=[char_row])
        on_click = char_msg.create_click_listener(timeout=60)

        @on_click.no_checks()
        async def chose_character(char_inter):
            f.update({"character_name": char_inter.component.label})

        beast_msg = await inter.reply("Which Beast?", components=[beast_row])
        on_click = beast_msg.create_click_listener(timeout=60)

        @on_click.no_checks()
        async def chose_beast(beast_inter):
            f.update({"beast_name": beast_inter.component.label})

        outcome_msg = await inter.reply("Outcome?", components=[
            ActionRow(Button(style=ButtonStyle.success, label="Win", custom_id="win"),
                      Button(style=ButtonStyle.danger, label="Loss", custom_id="loss"),
                      Button)
        ])



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

#TODO. do checks for Win, Loss, Tie


def setup(bot):
    bot.add_cog(ArenaCommands(bot))
