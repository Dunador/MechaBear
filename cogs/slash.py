from discord.ext import commands
from dislash import slash_command, ActionRow, Button, ButtonStyle, ResponseType


class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # Example of a slash command in a cog
    # @slash_command(description="Says Hello")
    # async def hello(self, inter):
    #     await inter.respond("Hello from cog!")
    #
    # # Buttons in cogs (no changes basically)
    # @commands.command()
    # async def button_test(self, ctx):
    #     row_of_buttons = ActionRow(
    #         Button(
    #             style=ButtonStyle.green,
    #             label="Green button",
    #             custom_id="green"
    #         ),
    #         Button(
    #             style=ButtonStyle.red,
    #             label="Red button",
    #             custom_id="red"
    #         )
    #     )
    #     msg = await ctx.send("This message has buttons", components=[row_of_buttons])
    #
    #     # Wait for a button click
    #     def check(inter):
    #         return inter.author == ctx.author
    #
    #     inter = await msg.wait_for_button_click(check=check)
    #     # Process the button click
    #     await inter.reply(f"Button: {inter.button.label}", type=ResponseType.UpdateMessage)


def setup(bot):
    bot.add_cog(SlashCommands(bot))
