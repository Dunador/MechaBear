import discord
from main import bot as client
from re import search, IGNORECASE
from datetime import datetime


def m_search(ctx, fuzzy_string):
    if type(fuzzy_string) is str:
        for g in client.guilds:
            if ctx.guild == g:
                for m in g.members:
                    if search(str(fuzzy_string), str(m.display_name), flags=IGNORECASE) and not m.bot:
                        return m
    elif type(fuzzy_string) is discord.Member:
        return fuzzy_string
    else:
        return False


async def insert_transaction(ctx, transaction, data, f):
    """
    :param ctx:
    :param transaction: str name of the transaction
    :param data: what the transaction did
    :param f: just pass f
    """
    t = {'exec_by': str(ctx.author.id), 'transaction': transaction, 'data': data, 'timestamp': datetime.utcnow()}
    await db.RobBot.transactions.insert_one({**t, **f})
