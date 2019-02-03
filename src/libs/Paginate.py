
import typing, types, discord

from libs.Tools import NoReactMethod

class NoReactMethod(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Paginated:
    def __init__(
        self, bot, message,
        member, react_map,
        timeout   = 60,
        on_start  = None,
        on_close  = None,
        on_error  = None
    ):
        """
        Pagination class

        keyword arguments
        -----------------
        members: list[discord.Member | discord.User]
            collection of members allowed to paginate the session

        message: discord.Message
            message containing the pagination session

        react_map dict{str: function}
            dictionary of reactions, and the functions to call when they're heard

        on_start: coroutine
            called when pagination is started

        on_close: coroutine
            called when pagination is ended

        on_error: coroutine
            called when there is an error handled that closes the paginator
        """
        self.backgroud_task = None

        if isinstance(bot, discord.Client):
            self.bot = bot
        else:
            raise TypeError(f"bot must be discord.User, not {type(bot)}")

        if isinstance(message, discord.Message):
            self.message = message
        else:
            raise TypeError(f"message must be a discord.Message, not a {type(message)}")

        if isinstance(member, (list, tuple, set)):
            self.member_ids = [m.id for m in members]
        if isinstance(member, (discord.User, discord.Member)):
            self.member_ids = {member.id}
        else:
            raise TypeError(f"member must be discord.User or list[discord.User], not {type(member)}")

        self.timeout = int(timeout)
        self.on_start = on_start
        self.on_close = on_close
        self.on_error = on_error
        self.react_map = react_map

    def check(self, reaction, user):
        if user.id not in self.member_ids or reaction.message.id != self.message.id:
            return False
        return reaction.emoji in self.react_map.keys()

    async def watcher(self):
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                check = self.check,
                timeout = self.timeout
            )
        except:
            await self.close()
        else:
            try:
                await self.message.remove_reaction(reaction, user)
                await self.react_map[reaction.emoji]()
                self.backgroud_task = self.bot.loop.create_task(self.watcher())
            except IndexError:
                if self.on_error:
                    await self.on_error(NoReactMethod)
                    self.close()
                else:
                    raise NoReactMethod

    async def start(self):
        try:
            if self.on_start:
                await self.on_start()
            for reaction in self.react_map.keys():
                await self.message.add_reaction(reaction)
            self.backgroud_task = self.bot.loop.create_task(self.watcher())
        except Exception as error:
            if self.on_error:
                await self.on_error(error)
                await self.close()
            else:
                raise error

    async def close(self):
        try:
            await self.message.clear_reactions()
        except discord.errors.NotFound:
            pass
        if self.backgroud_task:
            self.backgroud_task.cancel()
        if self.on_close:
            await self.on_close()
