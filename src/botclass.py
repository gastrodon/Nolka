from libs import Tools
from discord.ext import commands

class CachedBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mods = Tools.Mods()
        self.ongoing = set()

    async def update_modsquad(self):
        for guild in self.guilds:
            await self.mods.setup(guild)
