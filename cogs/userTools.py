import json

from discord.ext import commands


class UserCommands(commands.Cog, name='User Commands'):
    """
  User Commands
  """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(  # Decorator to declare where a command is.
        name='test',  # Name of the command, defaults to function name.
        aliases=['tst']  # Aliases for the command.
    )
    async def test(self, ctx):
      """
  Runs a test command
  """
        await ctx.send('Done')  # Sends a message where content='Done'

    @commands.command(name='earn', aliases=['save'])
    async def earn(self, ctx, amt):
      """
  CREATE / UPDATE
  """
        me = ctx.author  # sets me to your Member
        userdata = {}
        if me.id not in db.keys():  # CREATE: checks to see if there is a key with your ID first
            userdata["coins"] = 0
            # db[me.id] = json.dumps(userdata)

        userdata = json.loads(db[me.id])  # UPDATE: loads the prev coins and adds the new ones
        newcoins = int(amt) + userdata["coins"]
        userdata.update({"coins": newcoins})
        # db[me.id] = json.dumps(userdata)
        await ctx.send(f"{me.name} just saved {amt} coins for a total of {newcoins}")

    @commands.command(name='coins', aliases=['coinslist'])
    async def coins(self, ctx):
      """
  READ
  """
        me = ctx.author
        # userdata = json.loads(db[me.id])
        await ctx.send(f" {me.name} has a total of {userdata['coins']} coins ")

    @commands.command(name='spend', aliases=['coinspend'])
    async def spend(self, ctx, amt):
      """
  UPDATE
  """
        me = ctx.author
        userdata = json.loads(db[me.id])
        oldcoins = userdata["coins"]
        newcoins = oldcoins - int(amt)
        userdata.update({"coins": newcoins})
        # db[me.id] = json.dumps(userdata)
        await ctx.send(f"{me.name} just spent {amt} points for a total of {newcoins}")

    @commands.command(name='listall', aliases=['allcoins'])
    async def listall(self, ctx):
      """
  READ all coins
  """
        returnstr = f''
        """
    for key, coins in db.items():
      returnstr += f'{key} has {coins["coins"]} coins\n' """
        await ctx.send(
            f'{returnstr if ctx.author.id == self.bot.author_id else "I cannot allow you to do that, Dave."}')


def setup(bot):
    bot.add_cog(UserCommands(bot))
