from discord.ext import commands
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

    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        # check to see if the triggers are there
        #
        f = {'member_id': str(message.author.id), 'server_id': str(message.author.guild.id)}
        if message.content.startswith("@@"):
            # get the raw message to repeat
            message = message.content.replace("@","")
            # setup the channel to send to, change this later
            channel = client.get_channel(875590006192893982)

            # get the info from the database
            settings = await db.RobBot.peregrine.find_one(f)
            print(settings)
            #setup the webhook at that channel
            webhook = await channel.create_webhook(name=settings['name'])
            await webhook.send(message, avatar_url=settings['url'])
            await webhook.delete()

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

        def check(m):
            return m.author == ctx.author

        msg = await client.wait_for('message', check=check, timeout=30)
        await msg.delete()
        msg = "@"+msg.content
        await ctx.send('what is the image url?')

        url = await client.wait_for('message', check=check, timeout=30)
        await url.delete()
        url = url.content
        print(url)
        f = {'member_id': str(ctx.author.id), 'server_id': str(ctx.guild.id)}
        await db.RobBot.peregrine.update_one(f, {"$set": {"name": msg, "url": url}}, upsert=True)
        await ctx.send('Setup Complete. use @ text @')

#TODO: The plan is to have a listener for @, and have a list of which ones belong to who. then post to peregrine post


def setup(bot):
    bot.add_cog(TwitterCommands(bot))
