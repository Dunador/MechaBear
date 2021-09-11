from dislash import InteractionClient
from discord.ext import commands
import discord
import motor.motor_asyncio
import bot_config as config
####
from dislash import *

db = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb+srv://{config.DB_USER}:{config.DB_PASSWORD}@{config.MONGO_URL}")

intents = discord.Intents(
    guilds=True, members=True, messages=True, reactions=True,
    bans=False, emojis=False, integrations=False, webhooks=True, invites=False, voice_states=False, presences=False,
    typing=False
)

bot = commands.Bot(
    command_prefix="?",
    case_insensitive=True,
    intents=intents
)

i_client = InteractionClient(bot, test_guilds=config.SLASH_GUILDS)

bot.author_id = config.BOT_AUTHOR_ID


@bot.event
async def on_ready():
    print("I'm in")
    print(bot.user)


extensions = ['cogs.characters', 'cogs.owner', 'cogs.devTools', 'cogs.twitter', 'cogs.arena', 'cogs.help',
              'cogs.highlights', 'cogs.guilds', 'cogs.slash']

for extension in extensions:
    bot.load_extension(extension)

token = config.TOKEN
bot.run(token)

# TODO: add a way to add Crafters Certification
# TODO: connect names of characters to levels so that you can build your name
# TODO: Role Sign-up, # Welcome Questionnaire # Character Submission # VSheet Application # Quest Tag —> Role-sign-up
