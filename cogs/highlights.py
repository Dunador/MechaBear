from disnake.ext import commands
from disnake import Embed, Color
from main import bot as client


class HighlightsCommands(commands.Cog, name='Highlights Commands'):

    def __init__(self, bot):
        self.bot = bot

    @message_command(name="Send to Highlights")
    async def highlight(self, inter: ContextMenuInteraction):
        channel = client.get_channel(880270141710024745)
        webhooks = await channel.webhooks()
        if "MechaBear Highlighter" not in [w.name for w in webhooks]:
            webhook = await channel.create_webhook(name="MechaBear Highlighter")
        else:
            for w in webhooks:
                if w.name == "MechaBear Highlighter":
                    webhook = w

        if inter.message.embeds:
            e = Embed(type="rich", colour=Color.orange())
            e.set_thumbnail(url=inter.message.author.avatar_url)
            e.description = f'[here]({inter.message.jump_url})'
            e.add_field(name="Original Poster", value=inter.message.author.mention, inline=True)
            e.add_field(name="In Channel", value=inter.channel.mention, inline=True)
            e.add_field(name="Original Message", value=f'> {inter.message.content}', inline=False)
            e.set_footer(text=f"from {inter.message.created_at.date()}")
            await webhook.send(embed=e)
            await webhook.send(embeds=inter.message.embeds)
        else:
            e = Embed(type="rich", colour=Color.orange())
            e.set_thumbnail(url=inter.message.author.avatar_url)
            e.description = f'[here]({inter.message.jump_url})'
            e.add_field(name="Original Poster", value=inter.message.author.mention, inline=True)
            e.add_field(name="In Channel", value=inter.channel.mention, inline=True)
            e.add_field(name="Original Message", value=f'> {inter.message.content}', inline=False)
            e.set_footer(text=f"from {inter.message.created_at.date()}")
            e.set_image(url=inter.message.attachments[0].url)
            await webhook.send(embed=e, avatar_url='https://i.imgur.com/rFujonc.jpg')
        return await inter.reply("Message sent to the Highlight Reel", ephemeral=True)


def setup(bot):
    bot.add_cog(HighlightsCommands(bot))
