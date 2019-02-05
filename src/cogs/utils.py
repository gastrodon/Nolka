from libs import Macro, Paginate
from discord import Permissions
from discord.ext import commands
from discord.utils import oauth_url
from libs.Tools import CustomPermissionError
from random import randrange

class Helper:
    def __init__(self, ctx, message):
        self.paginator = Paginate.Paginated(
            bot = ctx.bot,
            message = message,
            member = ctx.author,
            react_map = {
                "\U000025c0": self.prev,
                "\U000025b6": self.next,
                "\U000023f9": self.stop
            },
            on_start = self.edit_message
        )

        self.ctx = ctx
        self.message = message
        self.size = 3
        self.index = 0
        self.help_items = self.generate_help()
        self.total = -(-len(self.help_items) // self.size)

    def generate_help(self):
        help_items = {}
        for command in self.ctx.bot.commands:
            if isinstance(command, commands.Group):
                for sub_com in command.commands:
                    docstring = sub_com.help if sub_com.help else "No docstring"
                    help_items[command.name + " " + sub_com.name] = docstring

            else:
                docstring = command.help if command.help else "No docstring"
                help_items[command.name] = docstring
        return help_items

    async def build_message(self):
        start = self.index * self.size
        end = min(start + self.size, len(self.help_items.keys()))
        final = await Macro.send("Help")
        final.title = f"{self.index + 1} of {self.total} pages | {len(self.help_items.keys())} total commands"
        for item in list(self.help_items.keys())[start:end]:
            if isinstance(item, dict):
                for subitem in list(item.keys()):
                    final.add_field(
                        name = f"{subitem}", value = item[subitem], inline = False
                    )
            final.add_field(
                name = f"{item}", value = self.help_items[item], inline = False
            )
        return final

        #for item in list()

    async def start(self):
        await self.paginator.start()

    async def prev(self):
        self.index = (self.index - 1 + self.total) % self.total
        await self.edit_message()

    async def next(self):
        self.index = (self.index + 1 + self.total) % self.total
        await self.edit_message()

    async def stop(self):
        await self.ctx.message.delete()
        await self.message.delete()
        await self.paginator.close()

    async def edit_message(self):
        await self.message.edit(
            embed = await self.build_message()
        )

class Utils:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def help(self, ctx):
        """
        Ask Nolka for help
        `-help`
        """
        message = await ctx.send(
            embed = await Macro.send("Getting help")
        )

        helper = Helper(ctx, message)
        await helper.start()

    @commands.command(pass_context = True)
    async def invite(self, ctx, *args):
        """
        Return an OAuth link to add this bot to a server
        `-invite`
        """
        await ctx.channel.send(
            embed = await Macro.send("Add me to your server [here]({})".format(
                oauth_url(self.bot.user.id, permissions = Permissions(permissions = 268443702))
            ))
        )

    @commands.command(pass_context = True)
    async def report(self, ctx, *, report = None):
        """
        Report something to the bot owner `Zero#5200` so it appears in my channel
        `-report <something that happened with the bot ~~or your day~~>`
        """
        if not report:
            raise CustomPermissionError
        try:
            await ctx.bot.log.send(
                embed = await Macro.Embed.infraction(f"{ctx.author.name} from {ctx.guild} said this:\n{report}")
            )
        except Exception as error:
            await ctx.send(
                embed = await Macro.send("The report was not sent")
            )
            raise error
        await ctx.send(
            embed = await Macro.send("The report has been sent")
        )

    @commands.command(pass_context = True, aliases = ["rand"])
    async def random(self, ctx, *args):
        """
        Get a random number. Default is 0 to 10. One argument: 0 to argument. Two arguments: argument 1 to argument 2
        `-random [number] [number]`
        """
        try:
            args = tuple(map(int, args))
        except ValueError:
            args = ()
        if len(args) is 0:
            return await ctx.send(
                embed = await Macro.send(f"Random from 0 to 10: {randrange(0, 10)}")
            )

        if len(args) is 1:
            return await ctx.send(
                embed = await Macro.send(f"Random from 0 to {args[0]}: {randrange(0, args[0])}")
            )

        return await ctx.send(
            embed = await Macro.send(f"Random from {args[0]} to {args[1]}: {randrange(args[0], args[1])}")
        )


def setup(bot):
    bot.add_cog(Utils(bot))
