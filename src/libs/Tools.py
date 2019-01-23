import os

class CustomPermissionError(Exception):
    pass

class CustomPerms:
    self.cachedir = os.path.dirname(os.path.realpath(__file__)) + "/cache/"

    @classmethod
    async def load(cls):
        for guild_id in os.listdir(cls.cachedir):
