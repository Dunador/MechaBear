from disnake.ext import commands
import disnake
import motor.motor_asyncio
import bot_config as config
####
from dislash import *

intents = disnake.Intents(
    guilds=True, members=True, messages=True, reactions=True,
    bans=False, emojis=False, integrations=False, webhooks=True, invites=False, voice_states=False, presences=False,
    typing=False
)

bot = commands.Bot(
    command_prefix="?",
    case_insensitive=True,
    intents=intents
)
# instance of the database
db = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb+srv://{config.DB_USER}:{config.DB_PASSWORD}@{config.MONGO_URL}")
bot.__setattr__("db", db.RobBot)

i_client = InteractionClient(bot, test_guilds=config.SLASH_GUILDS)

bot.author_id = config.BOT_AUTHOR_ID


@bot.event
async def on_ready():
    print("I'm in")
    print(bot.user)


for cog in config.cogs:
    bot.load_extension(f'cogs.{cog[:-3]}')

token = config.TOKEN
bot.run(token)

# TODO: Role Sign-up, # Welcome Questionnaire # Character Submission # VSheet Application # Quest Tag —> Role-sign-up
