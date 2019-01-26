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

    async def update_reporting_channel(self, guild_id, channel_id):
        self.log = self.get_guild(guild_id).get_channel(channel_id)

    async def async_init(self):
        await self.update_reporting_channel()
        await self.update_modsquad()
