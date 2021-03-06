import traceback, discord
from libs import Macro, Tools
from discord.ext import commands
from datetime import datetime


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        ignored = (commands.CommandNotFound)

        if isinstance(error, ignored):
            return

        if isinstance(error,
                      (commands.MissingRequiredArgument, Tools.NoRolesGiven,
                       Tools.CustomPermissionError)):
            return await ctx.send(
                embed = await Macro.Embed.error("I'm missing some arguments"))

        if isinstance(error, (commands.BadArgument, commands.UserInputError)):
            return await ctx.send(
                embed = await Macro.Embed.error("Those arguments don't work"))

        if isinstance(error, commands.MissingPermissions):
            missing_perms = ", ".join(error.missing_perms)
            return await ctx.send(embed = await Macro.Embed.error(
                f"You don't have the `{missing_perms}` permission"))

        if isinstance(error, commands.CheckFailure):
            return await ctx.send(
                embed = await Macro.Embed.error("You can't do that"))

        if isinstance(error, discord.errors.Forbidden):
            return await ctx.send(
                embed = await Macro.Embed.error("I'm not allowed to do that"))

        if isinstance(error, Tools.RolesTooHigh):
            return await ctx.send(embed = await Macro.Embed.error(
                "Some of those roles are above mine"))

        if isinstance(error, Tools.NoValidSelfRoles):
            return await ctx.send(embed = await Macro.Embed.error(
                "You can't self assign any of these roles"))

        if isinstance(error, Tools.NotSFW):
            return await ctx.send(embed = await Macro.Embed.error(
                "This isn't allowed in SFW channels."))

        if isinstance(error, Tools.CannotPaginate):
            return await ctx.send(embed = await Macro.error(
                "The permission `manage_messages` is required for pagination"))

        await self.bot.log.send(embed = await Macro.Embed.report(
            "Autoreported from guild {} at {}\nMessage: {}\nException in command {}\n{} {}\n\n{}"
            .format(
                ctx.guild, datetime.now(), ctx.message.content, ctx.command,
                type(error), error, "\n".join(
                    traceback.format_exception(
                        type(error), error, error.__traceback__,
                        chain = False)))))


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
