from discord.ext import commands
from dislash import slash_command, ActionRow, Button, ButtonStyle, ResponseType, message_command, ContextMenuInteraction
import utils.checks as checks

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @message_command(description="Vsheet test")
    async def vsheet(self, inter: ContextMenuInteraction):
        if '!vsheet' not in inter.message.embeds[0].footer.text:
            return await inter.reply("This is not a `!vsheet`")
        full_sheet = inter.message.embeds[0].description.replace("*", "").split("\n")
        skills = [x for x in full_sheet if "Skill P" in x][0][21:].split(", ")
        print(skills)
        return await inter.reply(f'{skills}')

def setup(bot):
    bot.add_cog(SlashCommands(bot))
