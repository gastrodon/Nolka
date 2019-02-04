from discord.ext import commands

class CachedBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = kwargs["config"]
        self.token = self.config["token"]
        self.gelbooru_api = self.config["gelbooruAPI"]
        self.gelbooru_id = self.config["gelbooruID"]
        self.derpibooru_api = self.config["derpibooruAPI"]
        # a set of ongoing tasks, like a list
        self.ongoing = []

    async def async_init(self):
        self.log = self.get_channel(self.config["log"][1])
