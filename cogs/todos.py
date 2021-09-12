import discord
from dislash import *
from discord.ext import commands
from utils import checks
from main import db
from utils.helpers import *
from utils.menu_options import *
from datetime import datetime
from pymongo import ASCENDING


class TodoCommands(commands.Cog, name='Todo Commands'):

    def __init__(self, bot):
        self.bot = bot
        self.add_color = discord.Colour.green()
        self.del_color = discord.Colour.red()
        self.info_color = discord.Colour.orange()
        self.f = {}

    @slash_command(description="Add TODO to your list")
    async def todo(self, inter):
        self.f = {"member_id": str(inter.author.id), "server_id": str(inter.guild.id)}
        pass

    @todo.sub_command(description="Adds a TODO to your Board", options=[
                      Option("text", "The content of your TODO item", OptionType.STRING, required=True)])
    async def add(self, inter, text):
        f = {"text": text, "completed": False}
        c = 1
        await db.RobBot.todos.insert_one({**self.f, **f})
        # load all TODOs
        active_todos = db.RobBot.todos.find({**self.f, "completed": False}).sort('_id', ASCENDING)
        returnstr = f'```css\n'
        async for todo in active_todos:
            returnstr += f'[{c}] {todo["text"]}\n'
            c += 1
        returnstr += f'\n --end of list--```'
        return await inter.reply(returnstr)

    @todo.sub_command(description="View you TODO Board")
    async def view(self, inter):
        c = 1
        active_todos = db.RobBot.todos.find({**self.f, "completed": False}).sort('_id', ASCENDING)
        returnstr = f'```css\n'
        async for todo in active_todos:
            returnstr += f'[{c}] {todo["text"]}\n'
            c += 1
        returnstr += f'\n --end of list--```'
        return await inter.reply(returnstr)


def setup(bot):
    bot.add_cog(TodoCommands(bot))
