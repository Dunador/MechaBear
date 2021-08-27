import re
import discord
from main import bot as client
from re import search


def m_search(ctx, fuzzy_string):
    if type(fuzzy_string) is str:
        for g in client.guilds:
            if ctx.guild == g:
                for m in g.members:
                    if search(str(fuzzy_string), str(m.display_name), flags=re.IGNORECASE) and not m.bot:
                        return m
    elif type(fuzzy_string) is discord.Member:
        return fuzzy_string
    else:
        return False
