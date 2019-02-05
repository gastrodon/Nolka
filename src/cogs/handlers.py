import discord, sys, traceback
from libs import Macro, Tools
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

        if isinstance(error, (commands.MissingRequiredArgument, Tools.NoRolesGiven, Tools.CustomPermissionError)):
            return await ctx.send(
                embed = await Macro.Embed.error("I'm missing some arguments")
            )
        if isinstance(error, (commands.BadArgument, commands.UserInputError)):
            return await ctx.send(
                embed = await Macro.Embed.error("Those arguments don't work")
            )
        if isinstance(error, commands.MissingPermissions):
            missing_perms = ", ".join(error.missing_perms)
            return await ctx.send(
                embed = await Macro.Embed.error(f"You don't have the `{missing_perms}` permission")
            )

        if isinstance(error, commands.CheckFailure):
            # I don't remember when this would be called
            return await ctx.send(
                embed = await Macro.Embed.error("You can't do that")
            )

        if isinstance(error, discord.errors.Forbidden):
            return await ctx.send(
                embed = await Macro.Embed.error("I'm not allowed to do that")
            )
        await self.bot.log.send(
            embed = await Macro.Embed.report(
                "Autoreported from guild {} at {}\nMessage: {}\nException in command {}\n{} {}\n\n{}".format(
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

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
