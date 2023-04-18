import platform
import discord
from discord.ext import commands
from utility import *


# Discord API bot
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='--', intents=discord.Intents().all())
        self.cog_list = ['cogs.cmds']

    # Performs setup during login
    async def setup_hook(self) -> None:
        for cog in self.cog_list:
            await self.load_extension(cog)

    # Called when bot is considered ready
    async def on_ready(self) -> None:
        ts = get_timestamp()
        print(f'{ts}Logged in as: {self.user}')
        print(f'{ts}Bot ID: {str(self.user.id)}')
        print(f'{ts}Discord version: {discord.__version__}')
        print(f'{ts}Python version: {str(platform.python_version())}')
        cmds = await self.tree.sync()
        print(f'{ts}Commands synced: {len(cmds)}')


bot = Bot()
token = get_token()


if __name__ == '__main__':
    bot.run(token)
