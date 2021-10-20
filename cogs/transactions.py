import disnake
from disnake.ext import commands
from utils.helpers import m_search
from utils import checks
from main import db


class TransactionLogs(commands.Cog, name='Transactions'):
    """These are the transaction log commands commands"""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_admin()
    @commands.command(name="checklog")
    async def check_log(self, ctx, member, n=10):
        await ctx.message.delete()
        member = m_search(ctx, member)
        returnstr = ''
        f = {'exec_by': str(member.id), 'server_id': str(ctx.guild.id)}
        results = db.RobBot.transactions.find(filter=f, sort=[("timestamp", -1)])
        for transaction in await results.to_list(length=10):
            returnstr += f'On {transaction["timestamp"].date()}, {member.display_name} executed a ' \
                         f'{transaction["transaction"]} command with data {transaction["data"]} \n'

        await ctx.send(returnstr)


def setup(bot):
    bot.add_cog(TransactionLogs(bot))
