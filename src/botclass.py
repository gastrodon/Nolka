from libs import Tools
from discord.ext import commands

class CachedBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = kwargs["config"]
        self.token = self.config["token"]
        self.gelbooru_api = self.config["gelbooruAPI"]
        self.gelbooru_id = self.config["gelbooruID"]
        # create an instance of a mods() object for moderators
        self.mods = Tools.Mods()
        # a set of ongoing tasks, like a list
        self.ongoing = set()

    async def update_modsquad(self):
        for guild in self.guilds:
            await self.mods.setup(guild)

    async def async_init(self):
        await self.update_modsquad()
        self.log = self.get_channel(self.config["log"][1])
