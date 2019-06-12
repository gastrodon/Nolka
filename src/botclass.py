import os, json
from libs import Macro
from discord.ext import commands
from datetime import datetime

class CachedBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = DiscordCache(self, "__cache")

        _config = kwargs["config"]
        self.token = _config["token"]
        self.gelbooru_api = _config["gelbooruAPI"]
        self.gelbooru_id = _config["gelbooruID"]
        self.derpibooru_api = _config["derpibooruAPI"]
        self.user_agent = _config["e621Agent"]
        self.__log_id = _config["log"]

    async def async_init(self):
        self.log = self.get_channel(self.__log_id)
        for guild in self.guilds:
            await self.flag_set(guild)

    async def add_self_roles(self, ctx, *roles):
        await self.cache.add_self_roles(ctx, roles)

    async def remove_self_roles(self, ctx,  *roles):
        await self.cache.remove_self_roles(ctx, roles)

    async def set_prefix(self, ctx, *prefixes):
        await self.cache.set_prefix(ctx, prefixes)

    async def add_prefix(self, ctx, *prefixes):
        await self.cache.add_prefix(ctx, prefixes)

    async def clear_prefix(self, ctx):
        await self.cache.clear_prefix(ctx)

    async def flag_set(self, guild):
        return await self.cache.flag_set(guild)

    async def flag_clear(self, guild):
        return await self.cache.flag_clear(guild)

    async def flag_check(self, guild):
        return await self.cache.flag_clear(guild)

    async def send_debug(self, message):
        await self.log.send(
            embed = Macro.debug(f"debug on {datetime.now()}\n\n{message}")
        )


class DiscordCache:
    def __init__(self, client, relative_path):
        self.path = f"{os.path.dirname(os.path.realpath(__file__))}/{relative_path}"
        self.filename = "cache.json"
        self.client = client

        if not os.path.isdir(self.path):
            os.mkdir(self.path)

        try:
            self.__cache = json.load(open(f"{self.path}/{self.filename}", "r"))

        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.__cache = {}

            with open(f"{self.path}/{self.filename}", "w") as stream:
                json.dump(self.__cache, stream)

    def __repr__(self):
        return json.dumps(self.__cache)

    async def write_cache(self):
        with open(f"{self.path}/{self.filename}", "w") as stream:
            json.dump(self.__cache, stream)

    async def new_guild(self, guild_id):
        self.__cache[guild_id] = {}
        await self.write_cache()

    async def add_self_roles(self, ctx, roles):
        guild = str(ctx.guild.id)

        if guild not in self.__cache:
            await self.new_guild(guild)

        add = [role.id for role in roles]
        existing = self.__cache[guild].get("self_roles", [])
        self.__cache[guild]["self_roles"] = [*add, *existing]
        await self.write_cache()

    async def remove_self_roles(self, ctx, roles):
        guild = str(ctx.guild.id)

        if guild not in self.__cache:
            await self.new_guild(guild)

        remove = [role.id for role in roles]
        self.__cache[guild]["self_roles"] = [role for role in self.__cache[guild]["self_roles"] if role not in remove]
        await self.write_cache()

    async def set_prefix(self, ctx, prefixes):
        guild = str(ctx.guild.id)

        if guild not in self.__cache:
            self.new_guild(guild)

        self.__cache[guild]["prefix"] = prefixes
        await self.write_cache()

    async def add_prefix(self, ctx, prefixes):
        current = await self.client.command_prefix(ctx.bot, ctx.message)
        await self.set_prefix(ctx, [*prefixes, *current])

    async def clear_prefix(self, ctx):
        await self.set_prefix(ctx, ["-"])

    async def prefix(self, message):
        guild = str(message.guild.id)

        if guild not in self.__cache:
            await self.new_guild(guild)

        return self.__cache[guild].get("prefix", ["-"])

    async def flag_set(self, guild):
        guild = str(guild.id)

        if guild not in self.__cache:
            await self.new_guild(guild)

        self.__cache[guild]["flag"] = True
        await self.write_cache()

    async def flag_clear(self, guild):
        guild = str(guild.id)

        if guild not in self.__cache:
            await self.new_guild(guild)

        self.__cache[guild]["flag"] = False
        await self.write_cache()

    async def flag_check(self, guild):
        guild = str(guild.id)

        if guild not in self.__cache:
            return False

        return self.__cache[guild],get("flag", False)

    def __getitem__(self, key):
        return self.__cache[key]
