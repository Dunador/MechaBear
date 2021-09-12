from discord.ext import commands
from dislash import *
from discord import Embed, Color
from utils.pagination import Element
import asyncio

class HelpCommands(commands.Cog, name='Help Commands'):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="The Official How-To Book")
    async def help(self, ctx):
        # the hardcoded how to
        menu = Element(header="Desternia How-To", long_desc="Find your Help Topic", elements=[
            Element(header="1. Rules and Regulations",
                    long_desc="You can find all the rules here Server <#772321868484968458>"),
            Element(header="2. Character Creation",
                    long_desc="Step by Step for creation of player characters. All official published Races and Classes allowed plus additional.", elements=[
                    Element(header="Levels",
                            long_desc="You can make create a characte starting at Level 1 through Level 3"),
                    Element(header="Races",
                            long_desc="All Official Races are allowed, and including the following here [link to other races]"),
                    Element(header="Classes",
                            long_desc="All Official Classes allowed, no HomeBrew / UA"),
                    Element(header="Stats",
                            long_desc="The only two Stat generation options is `Point Buy` or `Standard Array`", elements=[
                            Element(header="Point Buy",
                                    long_desc='Basically, all 6 of your ability scores start at 8, and you have 27 points to add to those scores however you’d like up to a maximum of 15.\n' \
                                              'Where it gets wonky is the top end of the scale, where it costs 2 points instead of 1 to go up to scores of 14 and 15.' \
                                              'Remember that it’s only the ability score modifiers that really matter. I feel like a lot of newer players have trouble ' \
                                              'figuring out what to do with that Ability Score Point Cost table because it leaves off the actual important part, which is ' \
                                              'what modifiers you’re buying for your points[Point Buy Calculator](https://chicken-dinner.com/5e/5e-point-buy.html)'),
                            Element(header="Standard Array",
                                    long_desc='`Standard array` means that there are no variables in character '
                                              'creation. No randomness, no change. You have 6 numbers that you slot '
                                              'into your character sheet before you add your racial bonuses.\n\n The '
                                              'numbers are as follows; 15, 14, 13, 12, 10, 8')
                        ])
                ]),
            Element(header="3. Roles", long_desc="Get your Roles to decide what channels you can view here <#772326263527309322>"),
            Element(header="4. Role Play", long_desc="There are different ways to start RolePlay", elements=[
                Element(header="Role Play Formatting", long_desc="Normal formatting for role play is ```standard text "
                                                                 "when doing things\n*italics when thinking "
                                                                 "things*\n**bold to empahize a word**\n\"quotes for "
                                                                 "things your character says\"(parenthesis for out of "
                                                                 "character or 4th wall things)\nand ||pipes when "
                                                                 "whispering or speaking a different language||```"),
                Element(header="Setting up NPC", long_desc="You can use either RodBot or Tuppper for your in "
                                                           "character. \n\n Rodbot \n`/npc add handle \"character "
                                                           "name\" http://url`\n\nand then use it like this: \n`/npc "
                                                           "handle \"words words\"`\n\nTupper:\n`tul!register "
                                                           "\"character name\" handle:text` <- upload your picture "
                                                           "with the message\n\nUse with: `handle:\"words words\""),
                Element(header="Starting RP", long_desc="You can start RP in the following channels:", elements=[
                    Element(header="Basement", long_desc="You can start by getting rifted in the Basement in <#772657394173607938>"),
                    Element(header="Badlands", long_desc="Join a campaign in <#806687342475477002>")])])])

        # Build buttons
        button_row_1 = ActionRow(Button(style=ButtonStyle.blurple, emoji="⬆", custom_id="up"),
                                 Button(style=ButtonStyle.green, label="Select", custom_id="select"))
        button_row_2 = ActionRow(Button(style=ButtonStyle.blurple, emoji="⬇", custom_id="down"),
                                 Button(style=ButtonStyle.red, label="Back", custom_id="back"))

        # Send a message with buttons
        emb = Embed(
            title=menu.header,
            description=f"{menu.long_desc}\n\n{menu.display_elements()}"
        )
        msg = await ctx.send(embed=emb, components=[button_row_1, button_row_2])

        # Click manager usage

        on_click = msg.create_click_listener(timeout=60)

        @on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
        async def on_wrong_user(inter):
            await inter.reply("You're not the author", ephemeral=True)

        @on_click.matching_id("down")
        async def down(inter):
            menu.next_elem()

        @on_click.matching_id("up")
        async def up(inter):
            menu.prev_elem()

        @on_click.matching_id("select")
        async def select(inter):
            nonlocal menu
            menu = menu.element

        @on_click.matching_id("back")
        async def back(inter):
            nonlocal menu
            menu = menu.parent

        @on_click.no_checks()
        async def response(inter):
            emb.title = menu.header
            emb.description = f"{menu.long_desc}\n\n{menu.display_elements()}"
            await inter.reply(embed=emb, type=ResponseType.UpdateMessage)

        @on_click.timeout
        async def on_timeout():
            for button in button_row_1.components:
                button.disabled = True
            for button in button_row_2.components:
                button.disabled = True
            await msg.edit(embed=emb, components=[button_row_1, button_row_2])


def setup(bot):
    bot.add_cog(HelpCommands(bot))
