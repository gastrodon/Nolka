
import typing, types, discord

from libs.Tools import NoReactMethod

class Paginated:
    def __init__(
        self,
        timeout   = 60,
        ctx       = None,
        message   = None,
        member    = None,
        react_map = None,
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
        self.backgrond_task = None

        self.ctx = ctx
        self.message = message
        self.member = member
        self.timeout = timeout
        self.on_start = on_start
        self.on_close = on_close
        self.on_error = on_error
        self.react_map = react_map

    def check(self, reaction, user):
        if user.id != self.member.id or reaction.message.id != self.message.id:
            return False
        return reaction.emoji in self.react_map.keys()

    async def watcher(self):
        try:
            reaction, user = await self.ctx.bot.wait_for(
                "reaction_add",
                check = self.check,
                timeout = self.timeout
            )
        except:
            await self.close()
        else:
            try:
                await self.message.clear_reactions()
                await self.react_map[reaction.emoji]()
                await self.start()
            except IndexError:
                raise NoReactMethod

    async def start(self):
        try:
            if self.on_start:
                await self.on_start()
            for reaction in self.react_map.keys():
                await self.message.add_reaction(reaction)
            self.backgrond_task = self.ctx.bot.loop.create_task(self.watcher())
        except Exception as error:
            if self.on_error:
                await self.on_error(error)
            await self.close()

    async def close(self):
        await self.message.clear_reactions()
        if self.backgrond_task:
            self.backgrond_task.cancel()
        if self.on_close:
            await self.on_close()
