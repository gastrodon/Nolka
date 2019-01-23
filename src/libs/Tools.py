import os, json, discord

class CustomPermissionError(Exception):
    pass

class NoSubcommand(Exception):
    pass

class CustomPerms:

    def __init__(self, cachedir = "__cache"):
        self.cachedir = os.path.dirname(os.path.realpath(__file__)) + "/{}/".format(cachedir)
        self.guild_map = {}
        self.load

    def check(ctx, permission):
        if permission not in self.guild_map[ctx.guild]:
            raise CustomPermissionError
        return ctx.author in self.guild_map[ctx.guild][permission]

    def add(ctx, permission, user):
        if permission not in self.guild_map[ctx.guild]:
            self.guild_map[ctx.guild][permission] = []
        if user in self.guild_map[ctx.guild][permission]:
            # TODO create a new error for this case
            raise CustomPermissionError
        self.guild_map[ctx.guild][permission].append(user)
        self.store()

    def remove(ctx, permission, user):
        if permission not in self.guild_map[ctx.guild]:
            raise CustomPermissionError
        del self.guild_map[ctx.guild][permission]
        self.store()

    def store(self):
        """
        { guild_object { permission_string { user_object_list } } }
        """
        for guild in self.guild_map:
            dump = {}
            for permission in guild:
                dump[permission] = [user.id for user in self.guild_map[guild][permission]]
            with open(guild.id, "w") as stream:
                json.dump(dump, stream)

    def load(self, bot):
        for guild_id in os.listdir(self.cachedir):
            guild = bot.get_guild(guild_id)
            self.guild_map[guild] = {}
            with open(cls.cachedir + guild_id) as stream:
                guild_permissions = json.load(stream)
                for permission in guild_permissions.items:
                    self.guild_map[guild][permission] = [bot.get_user(user_id) for user_id in guild_permissions[permission]]

    @classmethod
    async def load(cls, bot):
        perms_map = {}
        for guild_id in os.listdir(cls.cachedir):
            with open(cls.cachedir + guild_id) as stream:
                perms_map[bot.get_guild(guild_id)] = json.load(stream)
        return cls(guild_map = perms_map)

class Mods:
    def __init__(self, cachedir = "__cache"):
        self.cachedir = os.path.dirname(os.path.realpath(__file__)) + "/{}/".format(cachedir)
        self.guild_map = {}
        self.load

    def check(ctx):
        return ctx.message.author.id in self.guild_map[ctx.guild.id]
    def add(ctx, user):
        if ctx.guild.id not in self.guild_map:
            self.guild_map[ctx.guild.id] = {}
        self.guild_map[ctx.guild.id].append(user.id)
