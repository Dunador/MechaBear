import os

BOT_AUTHOR_ID = os.environ.get('BOT_AUTHOR_ID')

TOKEN = os.environ.get('TOKEN')
DB_USER = os.environ.get('DB_USER')
DB_NAME = os.environ.get('DB_NAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
MONGO_URL = os.environ.get('MONGO_URL')
MONGO_DB = os.environ.get('MONGO_DB')
# DEFAULT_STATUS = os.environ.get('DISCORD_STATUS', f'API')

SLASH_GUILDS = [435645321029353472]

# cogs
cogs = os.listdir("./cogs")
cogs.remove("__pycache__") if "__pycache__" in cogs else 0