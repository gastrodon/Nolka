"""
Server management for a bot named Nolka
"""

import discord, typing
from libs import Macro, Messages, Checks
from discord.ext import commands

class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True)
    @commands.check(Checks.manage_roles)
    async def role(self, ctx):
        """
        Group for manipulating guild roles.
        """
        if ctx.invoked_subcommand is None:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.noSubcommand)
            )

    @role.command(pass_context = True, aliases = ["create", "new"])
    async def give(self, ctx, *args):
        """
        Give roles to guild members. If they don't exist, create them.
        Takes a mixture of roles and @mentions and requires at least one new or existing role.
        """
        roles = [role for role in ctx.guild.roles if str(role) in args]
        members = [member for member in ctx.guild.members if member.mention in args]
        # TODO: use a generator to make a list of new roles
        for arg in args:
            if arg.lower() not in [str(role).lower() for role in roles] and "@" not in arg:
                roles.append(await ctx.guild.create_role(name = arg))
        if len(roles) is 0:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.missingArgs)
            )
            return
        if len(members) is 0:
            await ctx.channel.send(
                embed = await Macro.Embed.message(Messages.rolesMade.format(
                    ", ".join(map(str, roles))
                ))
            )
            return
        for member in members:
            await member.add_roles(*roles)
        await ctx.channel.send(
            embed = await Macro.Embed.message(Messages.rolesGiven.format(
                ", ".join(map(str, members)), ", ".join(map(str, roles))
            ))
        )

    @role.command(pass_context = True, aliases = ["remove"])
    async def take(self, ctx, *args):
        """
        Take roles from guild members.
        Takes a mixture of roles and @mentions and requires at least one of each.
        """
        roles = [role for role in ctx.guild.roles if str(role) in args]
        members = [member for member in ctx.guild.members if member.mention in args]
        if len(roles) is 0 or len(members) is 0:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.missingArgs)
            )
            return
        for member in members:
            await member.remove_roles(*roles)
        await ctx.channel.send(
            embed = await Macro.Embed.message(Messages.rolesTaken.format(
                ", ".join(map(str, members)), ", ".join(map(str, roles))
            ))
        )

    @role.command(pass_context = True, aliases = ["delete"])
    async def kill(self, ctx, *args):
        """
        Delete roles from the guild.
        Takes a list of roles and requires at least one
        """
        roles = [role for role in ctx.guild.roles if str(role) in args]
        if len(roles) is 0:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.missingArgs)
            )
            return
        for role in roles:
            await role.delete()
        await ctx.channel.send(
            embed = await Macro.Embed.message(Messages.rolesKilled.format(
                ", ".join(map(str, roles))
            ))
        )

    async def _notify(self, ctx, user, type, reason):
        if user.dm_channel is None:
            await user.create_dm()
        await user.dm_channel.send(
            embed = await Macro.Embed.infraction(
                Messages.removedGeneric.format(type, ctx.guild, reason)
            )
        )
        return

    @commands.command(pass_context = True, aliases = ["hammer"])
    @commands.check(Checks.ban_members)
    async def ban(self, ctx, user: typing.Union[discord.Member], *, reason = Messages.noReason):
        await self._notify(ctx, user, "banned", reason)
        await ctx.guild.ban(user, reason = reason)
        await ctx.send(
            embed = await Macro.Embed.infraction(Messages.goodbye.format(user.name))
        )


    @commands.command(pass_context = True)
    @commands.check(Checks.kick_members)
    async def kick(self, ctx, user: typing.Union[discord.Member], *, reason = Messages.noReason):
        await self._notify(ctx, user, "kicked", reason)
        await ctx.guild.kick(user, reason = reason)
        await ctx.send(
            embed = await Macro.Embed.infraction(Messages.goodbye.format(user.name))
        )

    @commands.command(pass_context = True)
    @commands.check(Checks.gaggle)
    async def mute(self, ctx, user: typing.Union[discord.Member], *, reason = Messages.noReason):
        pass

def setup(bot):
    bot.add_cog(Admin(bot))
