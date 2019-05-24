from discord.ext import commands
import os, json

class CachedBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = f"{os.path.dirname(os.path.realpath(__file__))}/__cache"
        self.config = kwargs["config"]
        self.token = self.config["token"]
        self.gelbooru_api = self.config["gelbooruAPI"]
        self.gelbooru_id = self.config["gelbooruID"]
        self.derpibooru_api = self.config["derpibooruAPI"]
        self.user_agent = self.config["e621Agent"]
        # a list of ongoing tasks
        self.ongoing = []

    async def async_init(self):
        await self.read_cache()
        self.log = self.get_channel(self.config["log"][1])

    async def new_cache(self):
        buffer = {}
        for guild in self.guilds:
            buffer[guild.id] = {}
        return buffer

    async def read_cache(self):
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        try:
            self.cache = json.load(open(f"{self.path}/cache.json", "r"))
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.cache = await self.new_cache()
            await self.update_cache()

    async def update_cache(self):
        with open(f"{self.path}/cache.json", "w") as stream:
            json.dump(self.cache, stream)

    async def add_self_roles(self, ctx, *roles):
        roles = [x.id for x in roles]
        self.cache[str(ctx.guild.id)]["self_roles"] = list(dict.fromkeys([*roles, *self.cache[str(ctx.guild.id)]["self_roles"]]))
        await self.update_cache()

    async def remove_self_roles(self, ctx, *roles):
        roles = [x.id for x in roles]
        self.cache[str(ctx.guild.id)]["self_roles"] = [role for role in self.cache[str(ctx.guild.id)]["self_roles"] if role not in roles]
        await self.update_cache()

    async def new_guild_cache(self, ctx):
        self.cache[str(ctx.guild.id)] = {}
        await self.update_cache()

    async def set_prefix(self, ctx, *prefixes):
        self.cache[str(ctx.guild.id)]["prefix"] = prefixes
        await self.update_cache()

    async def add_prefix(self, ctx, *prefixes):
        current = await self.command_prefix(ctx.bot, ctx.message)
        await self.set_prefix(ctx, *[*current, *prefixes])


    async def clear_prefix(self, ctx):
        del self.cache[str(ctx.guild.id)]["prefix"]
        await self.update_cache()
