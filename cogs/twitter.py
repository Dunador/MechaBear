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




    # @commands.Cog.listener("on_message")
    # async def on_message(self, message):
    #     # check to see if the triggers are there
    #     #
    #     f = {'member_id': str(message.author.id), 'server_id': str(message.author.guild.id)}
    #     if message.content.startswith("@@"):
    #         # get the raw message to repeat
    #         message = message.content.replace("@","")
    #         # setup the channel to send to, change this later
    #         channel = client.get_channel(875590006192893982)
    #
    #         # get the info from the database
    #         settings = await db.RobBot.peregrine.find_one(f)
    #         print(settings)
    #         #setup the webhook at that channel
    #         webhook = await channel.create_webhook(name=settings['name'])
    #         await webhook.send(message, avatar_url=settings['url'])
    #         await webhook.delete()

    # if "ice" in message.content.lower():
    #     webhook = await message.channel.create_webhook(name='IceBear(real)')
    #     url = 'https://cdn.discordapp.com/attachments/880270141710024745/881387965719404575/Ice_bear.webp'
    #     await webhook.send('Yes, IceBear loves you.', avatar_url=url)
    #     await webhook.delete()

    @commands.command(name="setup@")
    async def setup_twitter(self, ctx):
        """
        Sets up your @ handle and character
        """
        await ctx.send('What will be your @ name')

        def workflow_m_check(m):
            if m.author.id == ctx.author.id:
                return True

        msg = await client.wait_for('message', check=workflow_m_check, timeout=30)
        await msg.delete()
        msg = "@" + msg.content
        await ctx.send('what is the image url?')

        url = await client.wait_for('message', check=check, timeout=30)
        await url.delete()
        url = url.content
        print(url)
        f = {'member_id': str(ctx.author.id), 'server_id': str(ctx.guild.id)}
        await db.RobBot.peregrine.update_one(f, {"$set": {"name": msg, "url": url}}, upsert=True)
        await ctx.send('Setup Complete. use @ text @')


def setup(bot):
    bot.add_cog(TwitterCommands(bot))
