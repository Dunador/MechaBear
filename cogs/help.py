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
            Element(header="Rules and Regulations", long_desc="You can find all the rules here Server <#772321868484968458>"),
            Element(header="Roles", long_desc="Get your Roles to decide what channels you can view here <#772326263527309322>"),
            Element(header="Characters", long_desc="You can start building your character. Type `!initial` in <#772364979898417162>"),
            Element(header="Role Play", long_desc="There are different ways to start RolePlay", elements=[
                Element(header="Basement", long_desc="You can start by getting rifted in the Basement in <#772657394173607938>"),
                Element(header="Badlands", long_desc="Join a campaign in <#806687342475477002>")
                ]
            )
        ])
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
