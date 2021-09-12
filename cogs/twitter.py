from discord.ext import commands
from dislash import *
import discord
import utils.checks as checks
from main import db, bot as client
from utils.pipelines import profile_pipeline, mod_pipeline
from utils.helpers import *
from datetime import datetime


class TwitterCommands(commands.Cog, name='Peregrine'):
    """
  Commands for the post
  """

    def __init__(self, bot):
        self.bot = bot
        self.webhook = ''
        self.f = {}
        self.chars = []

    @slash_command(description="Peregrine Post Commands",
                   options=[Option("post", "Execute a Peregrine Post", required=True)])
    async def peregrine(self, inter, post):
        # vars
        f = {'member_id': str(inter.author.id), 'server_id': str(inter.guild.id)}
        db_entries = db.RobBot.characters.find({**f, "status": "alive"})
        channel = client.get_channel(875590006192893982)
        webhooks = await channel.webhooks()
        char_row = ActionRow()
        async for char in db_entries:
            char_row.add_button(style=ButtonStyle.green, label=char["name"], custom_id=char["name"].lower())
        # checks
        if "Peregrine Post" not in [w.name for w in webhooks]:
            webhook = await channel.create_webhook(name="Peregrine Post")
        else:
            for w in webhooks:
                if w.name == "Peregrine Post":
                    webhook = w
        # logic
        char_msg = await inter.reply("Which Character is Sending this?", components=[char_row])
        on_click = char_msg.create_click_listener(timeout=60)

        @on_click.no_checks()
        async def choice_is_made(choice_inter):
            await char_msg.delete()
            char_search = {"name": choice_inter.component.label}
            char = await db.RobBot.characters.find_one({**self.f, **char_search})
            await webhook.send(post ,username=char['handle'], avatar_url=char['imageurl'])


def setup(bot):
    bot.add_cog(TwitterCommands(bot))
