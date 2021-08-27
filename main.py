import os
from discord.ext import commands
import discord
import motor.motor_asyncio
import bot_config as config

db = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb+srv://{config.DB_USER}:{config.DB_PASSWORD}@{config.MONGO_URL}")


intents = discord.Intents(
    guilds=True, members=True, messages=True, reactions=True,
    bans=False, emojis=False, integrations=False, webhooks=False, invites=False, voice_states=False, presences=False,
    typing=False
)

bot = commands.Bot(
    command_prefix="?",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=intents
)
bot.author_id = config.BOT_AUTHOR_ID  # Change to your discord id!!!


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    g_guilds = bot.guilds


extensions = ['cogs.userTools', 'cogs.adminTools', 'cogs.devTools', 'cogs.tokens', 'cogs.points', 'cogs.characters',
              'cogs.guilds', 'cogs.MainQuest']

for extension in extensions:
    bot.load_extension(extension)  # Loads every extension.

# keep_alive()  # Starts a webserver to be pinged.
token = config.TOKEN
bot.run(token)  # Starts the bot

#TODO: delete the originating message