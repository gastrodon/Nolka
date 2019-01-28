import discord, sys, traceback
from libs import Macro, Messages, Tools
from discord.ext import commands
from datetime import datetime

class ErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        ignored = (commands.CommandNotFound, commands.UserInputError)

        if isinstance(error, ignored):
            return
            pass

        if isinstance(error, (commands.MissingRequiredArgument, Tools.NoRolesGiven)):
            await ctx.send(
                embed = await Macro.Embed.error(Messages.MissingRequiredArgument)
            )
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                embed = await Macro.Embed.error(Messages.BadArgument)
            )
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                embed = await Macro.Embed.error(Messages.MissingPermissions)
            )
            return

        if isinstance(error, commands.CheckFailure):
            await ctx.send(
                embed = await Macro.Embed.error(Messages.MissingPermissions)
            )
            return

        if isinstance(error, discord.errors.Forbidden):
            await ctx.send(
                embed = await Macro.Embed.error(Messages.Forbidden)
            )
            return
        await self.bot.log.send(
            embed = await Macro.Embed.report(
                Messages.traceback.format(
                    ctx.guild,
                    datetime.now(),
                    ctx.message.content,
                    ctx.command,
                    type(error),
                    error,
                    "\n".join(traceback.format_exception(type(error), error, error.__traceback__, chain=False))
                )
            )
        )

    async def on_guild_join(self, guild):
        await self.bot.mods.setup(guild)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
