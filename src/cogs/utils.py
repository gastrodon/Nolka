"""
Utility commands for a bot named Nolka
"""

from libs import Macro, Messages
from discord.ext import commands

class Utils:
    def __init__(self, bot):
        self.bot = bot


    @staticmethod
    def _unpackSubcommands(*botCommands):
        """
        Recursively unpack a group of commands
        """
        for command in botCommands:
            yield ["`{}`".format(command.name), command.help] if command.help else ["`{}`".format(command.name), Messages.noDocstring]
            if isinstance(command, commands.Group):
                for sub in command.commands:
                    yield ["`{}: {}`".format(command.name, sub.name), sub.help] if sub.help else ["`{}: {}`".format(command.name, sub.name), Messages.noDocstring]

    @staticmethod
    def _renderHelp(group):
        message = Messages.helpTemplate
        for item in group:
            if isinstance(item, commands.Group):
                message.append(_unpackSubcommands(item))

    @commands.command(pass_context = True)
    async def ping(self, ctx, count = 1):
        """
        Return the bot's latency
        """
        latency = self.bot.latency * 1000
        try:
            int(count)
        except ValueError:
            count = 1
        for _ in range(int(count)):
            await ctx.channel.send(
                embed = await Macro.Embed.message(
                    Messages.pingms.format(latency)
                )
            )

    @commands.command(pass_context = True)
    async def help(self, ctx, *args):
        """
        Ask Nolka for help
        """
        # TODO: List them 5 at a time and use reacts to scroll through them
        if len(args) is 0:
            helpitems = []
            messageDesc = Messages.helpTemplate
            for command in self._unpackSubcommands(*self.bot.commands):
                helpitems.append(command)
        await ctx.channel.send(
            embed = await Macro.Embed.help(
                messageDesc,
                helpitems
            )
        )

    @commands.command(pass_context = True)
    async def latest(self, ctx, *args):
        """
        Test to make sure that everything was updated
        """
        # TODO: This should not be hard coded, instead fetched from somewhere that I control
        await ctx.channel.send(
            embed = await Macro.Embed.message(
                Messages.latest
            )
        )


def setup(bot):
    bot.add_cog(Utils(bot))
