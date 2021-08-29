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
    command_prefix="?",
    case_insensitive=True,
    intents=intents
)
bot.author_id = config.BOT_AUTHOR_ID


@bot.event
async def on_ready():
    print("I'm in")
    print(bot.user)
    g_guilds = bot.guilds


extensions = ['cogs.userTools', 'cogs.adminTools', 'cogs.devTools', 'cogs.tokens', 'cogs.characters',
              'cogs.guilds', 'cogs.MainQuest', 'cogs.transactions', 'cogs.arena', 'cogs.twitter']

for extension in extensions:
    bot.load_extension(extension)


token = config.TOKEN
bot.run(token)

# TODO: make embeds