"""
Server management for a bot named Nolka
"""

import discord, typing, re
from libs import Macro, Messages, Tools
from discord.ext import commands
from asyncio import sleep

class Workers:
    @staticmethod
    def modcheck():
        def wrapped(ctx):
            return ctx.bot.mods.check(ctx)
        return commands.check(wrapped)

    @staticmethod
    async def _notify(ctx, user, type, reason):
        try:
            if user.dm_channel is None:
                await user.create_dm()
            await user.dm_channel.send(
                embed = await Macro.Embed.infraction(
                    Messages.removedGeneric.format(type, ctx.guild, reason)
                )
            )
            return
        except:
            return

    @staticmethod
    async def role_timer(ctx, user, role, duration):
        await ctx.send(
            embed = await Macro.send(Messages.muted.format(user.mention))
        )
        await user.add_roles(role)
        await sleep(duration)
        await user.remove_roles(role)
        await ctx.send(
            embed = await Macro.send(Messages.unmuted.format(user.mention))
        )

    @staticmethod
    async def mute_timer(ctx, user, duration, reason):
        for channel in ctx.guild.channels:
            await channel.set_permissions(
                user,
                reason = Messages.muted.format(ctx.author.name) + " " + Messages.reasonGiven.format(reason),
                send_messages = False,
                add_reactions = False
            )
        await ctx.send(
            embed = await Macro.send(
                Messages.muted.format(user.mention)
            )
        )
        await sleep(duration)
        for channel in ctx.guild.categories:
            await channel.set_permissions(
                user,
                reason = Messages.unmuted.format(ctx.author.name) + " " + Messages.reasonGiven.format(reason),
                send_messages = None,
                add_reactions = None
            )
        await ctx.send(
            embed = await Macro.send(
                Messages.unmuted.format(user.mention)
            )
        )

class Commands:
    def __init__(self, bot):
        self.bot = bot
        self.modcheck = self.bot.mods.check
        self.time_factors = {1, 60, 24}
        self.time_factors = {
            "d" : 86400,
            "h" : 3600,
            "m" : 60,
            "s" : 1
        }

    modcheck = Workers.modcheck

    @commands.group(pass_context = True)
    @modcheck()
    async def role(self, ctx):
        """
        Group for manipulating guild roles.
        """
        # TODO have this list user roles
        if ctx.invoked_subcommand is None:
            pass

    @role.command(pass_context = True, aliases = ["give", "new", "create"])
    async def role_give(self, ctx, *args : typing.Union[discord.Role, discord.Member, str]):
        """
        Used to create roles and assign roles.
        If new roles are passed in, they will be created.
        If new or existing roles and guild members are passed in, they will be created if applicable and assigned
        Takes a mixture of roles and guild members. Requires at least one new role, or one role and a guild member.
        """
        users = list(filter(lambda x : isinstance(x, discord.Member), args))
        roles = list(filter(lambda x : isinstance(x, discord.Role), args))
        new_roles = list(filter(lambda x : isinstance(x, str), args))
        if len(roles) + len(new_roles) is 0:
            raise discord.MissingRequiredArgument(discord.Role)
        for new in new_roles:
            new = await ctx.guild.create_role(name = new)
            roles.append(new)
        if len(new_roles) is not 0:
            await ctx.send(
                embed = await Macro.send(Messages.rolesMade.format(
                    ", ".join(new_roles)
                ))
            )
        if len(users) is 0:
            return
        for user in users:
            await user.add_roles(*roles)
        await ctx.send(
            embed = await Macro.send(Messages.rolesGiven.format(
                ", ".join(map(str, users)), ", ".join(map(str, roles))
            ))
        )

    @role.command(pass_context = True, aliases = ["take", "remove"])
    async def role_take(self, ctx, *args: typing.Union[discord.Role, discord.Member]):
        """
        Removes roles from guild members.
        Takes a mixture of roles and guild members. Requires at least one of each.
        """
        roles = list(filter(lambda x : isinstance(x, discord.Role), args))
        members = list(filter(lambda x : isinstance(x, discord.Member), args))
        if len(roles) is 0 or len(members) is 0:
            raise discord.MissingRequiredArgument(discord.Role if len(roles) is 0 else discord.Member)
        for member in members:
            await member.remove_roles(*roles)
        await ctx.channel.send(
            embed = await Macro.send(Messages.rolesTaken.format(
                ", ".join(map(str, members)), ", ".join(map(str, roles))
            ))
        )

    @role.command(pass_context = True, aliases = ["delete", "kill"])
    async def role_kill(self, ctx, *roles: typing.Union[discord.Role]):
        """
        Delete roles from the guild.
        Takes a list of roles. Requires at least one.
        """
        if len(roles) is 0:
            raise discord.MissingRequiredArgument(discord.Role)
        for role in roles:
            await role.delete()
        await ctx.channel.send(
            embed = await Macro.send(Messages.rolesKilled.format(
                ", ".join(map(str, roles))
            ))
        )

    @commands.command(pass_context = True, aliases = ["hammer"])
    @modcheck()
    async def ban(self, ctx, user: discord.Member, *, reason = Messages.noReason):
        await self._notify(ctx, user, "banned", reason)
        await ctx.guild.ban(user, reason = reason)
        await ctx.send(
            embed = await Macro.Embed.infraction(Messages.goodbye.format(user.name))
        )

    @commands.command(pass_context = True)
    @modcheck()
    async def kick(self, ctx, user: discord.Member, *, reason = Messages.noReason):
        await self._notify(ctx, user, "kicked", reason)
        await ctx.guild.kick(user, reason = reason)
        await ctx.send(
            embed = await Macro.Embed.infraction(Messages.goodbye.format(user.name))
        )

    @commands.command(pass_context = True)
    @modcheck()
    async def tempmute(self, ctx, user: typing.Union[discord.Member], duration, *, reason = Messages.noReason):
        """
        Mute a user for a set duration
        Accepts a guild member and a time duration in the format
        """
        try:
            self.bot.loop.create_task(Workers.mute_timer(ctx, user, int(duration), reason))
        except:
            pass
        try:
            duration = int(duration[0:-1]) * self.time_factors[duration[-1]]
            self.bot.loop.create_task(Workers.mute_timer(ctx, user, duration, reason))
        except:
            raise commands.BadArgument

    @commands.group(pass_context = True, aliases = ["modsquad", "squad"])
    @modcheck()
    async def mod(self, ctx):
        """
        Group for managing the ModSquad
        """
        if ctx.invoked_subcommand is None:
            pass

    @mod.command(pass_context = True, aliases = ["add"])
    async def mod_add(self, ctx, user: typing.Union[discord.Member]):
        """
        Add a user to the ModSquad
        Accepts and requires a guild member
        """
        await self.bot.mods.add(ctx, user)
        await ctx.send(
            embed = await Macro.send(Messages.modCreate.format(user.mention))
        )

    @mod.command(pass_context = True, aliases = ["remove"])
    async def mod_remove(self, ctx, user: typing.Union[discord.Member]):
        """
        Remove a user from the ModSquad
        Accepts and requires a guild member
        """
        await self.bot.mods.remove(ctx, user)
        await ctx.send(
            embed = await Macro.send(Messages.modRemove.format(user.mention))
        )


def setup(bot):
    bot.add_cog(Commands(bot))
