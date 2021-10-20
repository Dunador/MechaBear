from disnake.ext import commands
from disnake import Colour
from utils import checks


class VSheetCommands(commands.Cog, name='VSheet Commands'):

    def __init__(self, bot):
        self.bot = bot
        self.add_color = Colour.green()
        self.del_color = Colour.red()
        self.info_color = Colour.orange()
        self.f = {}

    @commands.Cog.listener()
    async def on_message(self, msg):
        # identify a VSheet from Avrae in the channel
        if msg.channel.id == 880270141710024745 and msg.author.id == 261302296103747584 and len(
                msg.embeds) != 0 and '!vsheet' in msg.embeds[0].footer.text:
            channel_sent = msg.channel
            # parse the information
            print(msg.embeds[0].author)
            full_sheet = msg.embeds[0].description.replace("*", "").split("\n")
            print(full_sheet)
            skills = [x for x in full_sheet if "Skill P" in x][0][21:].split(", ")
            print(skills)
            await channel_sent.send("That is a Vsheet")


def setup(bot):
    bot.add_cog(VSheetCommands(bot))
