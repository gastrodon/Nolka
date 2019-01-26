import os, json, discord, types

class CustomPermissionError(Exception):
    pass

class NoSubcommand(Exception):
    pass

class CacheReadError(json.decoder.JSONDecodeError):
    pass

class NoRolesGiven(Exception):
    pass

class Mods:
    def __init__(self, cachedir = "__cache"):
        self.cachedir = os.path.dirname(os.path.realpath(__file__)) + "/{}/".format(cachedir)
        self.guild_map = {}
        if not os.path.exists(self.cachedir):
            os.mkdir(self.cachedir)
        for guild_id in os.listdir(self.cachedir):
            self.load(guild_id)
    async def check(self, ctx):
        return ctx.message.author.id in self.guild_map[ctx.guild.id]
    async def add(self, ctx, user):
        self.guild_map[ctx.guild.id].add(user.id)
        await self.save(ctx.guild.id)
    async def remove(self, ctx, user):
        self.guild_map[ctx.guild.id].remove(user.id)
        await self.save(ctx.guild.id)
    async def setup(self, guild):
        self.guild_map[guild.id] = {guild.owner.id}
        await self.save(guild.id)
    async def save(self, guild_id):
        """
        { guild_id { user_ids } }
        """
        with open(self.cachedir + str(guild_id), "w") as stream:
            json.dump(list(self.guild_map[guild_id]), stream)
    def load(self, guild_id):
        with open(self.cachedir + str(guild_id)) as stream:
            self.guild_map[int(guild_id)] = set(json.load(stream))
