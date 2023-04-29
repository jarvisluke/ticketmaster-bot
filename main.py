import platform
import discord
import mysql.connector
from discord.ext import commands
from utility import *
import query


# Discord bot
class Bot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='-', intents=discord.Intents().all())
        self.cog_list = ['cogs.slash_cmd']

    # Performs setup during login
    async def setup_hook(self) -> None:
        # Loads commands in cogs
        for cog in self.cog_list:
            await self.load_extension(cog)

    # Called when bot is ready
    async def on_ready(self) -> None:
        print(f'{get_timestamp()}Logged in as: {self.user}')
        print(f'{get_timestamp()}Bot ID: {self.user.id}')
        print(f'{get_timestamp()}Discord version: {discord.__version__}')
        print(f'{get_timestamp()}Python version: {platform.python_version()}')
        cmds = await self.tree.sync()
        print(f'{get_timestamp()}Commands synced: {len(cmds)}')


# Creates MySQL connection
db = mysql.connector.connect(host='localhost', user='root', password=get_value('SQLKEY'), database='tm')
# Creates discord bot
bot = Bot()


# Called when a change is made to a member
@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    # TODO: update username in database if it changes
    added_role = False
    removed_role = False
    # Sets added_roles to any roles added to after
    for role in after.roles:
        if role not in before.roles:
            added_role = role
    # Sets removed to any roles removed from after
    for role in before.roles:
        if role not in after.roles:
            removed_role = role
    if added_role:
        query.create_tech(after)
    elif removed_role:
        query.remove_tech(after)


if __name__ == '__main__':
    token = get_value('TOKEN')
    bot.run(token)
