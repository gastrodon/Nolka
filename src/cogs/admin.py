"""
Server management for a bot named Nolka
"""

import discord, typing
from libs import Macro, Tools
from discord.ext import commands
from asyncio import sleep

class Workers:
    @staticmethod
    async def _notify(ctx, user, mode, reason):
        try:
            if user.dm_channel is None:
                await user.create_dm()
            await user.dm_channel.send(
                embed = await Macro.Embed.infraction(
                    f"You have been {mode} from the server {ctx.guild}\nReason given: {reason}"
                )
            )
            return
        except discord.Forbidden:
            return

    @staticmethod
    async def _mute_create(ctx):
        await ctx.send(
            embed = await Macro.send("Let me set up a `muted` role")
        )
        guild = ctx.guild
        role = await guild.create_role(name = "muted")
        for channel in guild.channels:
            await channel.set_permissions(
                role,
                reason = f"Created a mute role",
                send_messages = False,
                add_reactions = False
            )
        role.edit(position = guild.me.top_role.position - 1)
        return role

    @staticmethod
    async def mute_timer(ctx, user, duration):
        role = discord.utils.find(lambda x : x.name == "muted", ctx.guild.roles) or await Workers._mute_create(ctx)
        await user.add_roles(role)
        await ctx.send(
            embed = await Macro.send(f"Muted {user.name}")
        )
        await sleep(duration)
        await user.remove_roles(role)
        await ctx.send(
            embed = await Macro.send(f"Unmuted {user.name}")
        )

class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.time_factors = {
            "d" : 86400,
            "h" : 3600,
            "m" : 60,
            "s" : 1,
        }


    @commands.group(pass_context = True, aliases = ["roles"])
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            if len(ctx.author.roles[1:]):
                roles = list(map(str, ctx.author.roles[1:]))
                return await ctx.send(
                    embed = await Macro.send(f"You have the roles {', '.join(roles)}")
                )
            return await ctx.send(
                embed = await Macro.send("You have no special roles")
            )

    @role.command(pass_context = True, name = "give", aliases = ["new", "create"])
    @commands.has_permissions(manage_roles = True)
    async def role_give(self, ctx, *args : typing.Union[discord.Role, discord.Member, str]):
        """
        Used to create roles and assign roles.
        If new roles are passed in, they will be created. If new or existing roles and guild members are passed in, they will be created if applicable and assigned
        `-role give [roles] [users]`
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
                embed = await Macro.send(f"Created the roles {', '.join(new_roles)}")
            )
        if len(users) is 0:
            return
        for user in users:
            await user.add_roles(*roles)
        users = map(str, users)
        roles = map(str, roles)
        await ctx.send(
            embed = await Macro.send(f"Gave {', '.join(users)} the roles {', '.join(roles)}")
        )

    @role.command(pass_context = True, name = "take", aliases = ["remove"])
    @commands.has_permissions(manage_roles = True)
    async def role_take(self, ctx, *args: typing.Union[discord.Role, discord.Member]):
        """
        Removes roles from guild members.
        `-role take <roles> <users>`
        """
        roles = list(filter(lambda x : isinstance(x, discord.Role), args))
        members = list(filter(lambda x : isinstance(x, discord.Member), args))
        if len(roles) is 0 or len(members) is 0:
            raise discord.MissingRequiredArgument(discord.Role if len(roles) is 0 else discord.Member)
        for member in members:
            await member.remove_roles(*roles)
        members = map(str, members)
        roles = map(str, roles)
        await ctx.channel.send(
            embed = await Macro.send(f"The users {', '.join(members)} no longer have the roles {', '.join(roles)}")
        )

    @role.command(pass_context = True, name = "kill", aliases = ["delete"])
    @commands.has_permissions(manage_roles = True)
    async def role_kill(self, ctx, *roles: typing.Union[discord.Role]):
        """
        Delete roles from the guild.
        `-role kill <roles>`
        """
        if len(roles) is 0:
            raise discord.MissingRequiredArgument(discord.Role)
        if ctx.guild.me.top_role < max(roles):
            raise Tools.RolesTooHigh
        for role in roles:
            await role.delete()
        roles = map(str, roles)
        await ctx.channel.send(
            embed = await Macro.send(f"Killed the roles {', '.join(roles)}")
        )

    @commands.command(pass_context = True, aliases = ["hammer"])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user: discord.Member, *, reason = "No reason given"):
        """
        Bannes a user from a guild. Keep in mind that banned users cannot rejoin normally unless unbanned.
        `-ban <user> [reason]`
        """
        await Workers._notify(ctx, user, "banned", reason)
        await ctx.guild.ban(user, reason = reason)
        return await ctx.send(
            embed = await Macro.Embed.infraction(f"goodbye, {user.name}")
        )

    @commands.command(pass_context = True)
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: discord.Member, *, reason = "No reason given"):
        """
        Kickes a user from a guild. Keep in mind that kicked users can rejoin normally.
        `-kick <user> [reason]`
        """
        await Workers._notify(ctx, user, "kicked", reason)
        await ctx.guild.kick(user, reason = reason)
        return await ctx.send(
            embed = await Macro.Embed.infraction(f"goodbye, {user.name}")
        )

    @commands.command(pass_context = True)
    async def tempmute(self, ctx, user: typing.Union[discord.Member], duration):
        """
        Mute a user for a set duration
        `-tempmute <user> <number of d|h|m|s|> [reason]`
        """
        try:
            self.bot.loop.create_task(Workers.mute_timer(ctx, user, int(duration)))
        except ValueError:
            pass
        try:
            duration = int(duration[0:-1]) * self.time_factors[duration[-1]]
            self.bot.loop.create_task(Workers.mute_timer(ctx, user, duration))
        except:
            raise commands.BadArgument

def setup(bot):
    bot.add_cog(Admin(bot))
