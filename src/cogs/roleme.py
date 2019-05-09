"""
Server management for a bot named Nolka
"""

import discord, typing
from libs import Macro, Tools
from discord.ext import commands
from asyncio import sleep


class Roleme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True, name = "roleme", aliases = ["self"])
    async def roleme(self, ctx):
        """
        Base command for roleme commands, or standalone command for looking at self assignable roles.
        If called alone, will return roles that users can give themselves.
        `-roleme`
        """
        if ctx.invoked_subcommand is None:
            allowed = [f"`{ctx.guild.get_role(role)}`" for role in ctx.bot.cache[str(ctx.guild.id)]["self_roles"]]
            if len(allowed):
                return await ctx.send(
                    embed = await Macro.send(f"You can assign yourself the roles: {', '.join(allowed)}")
                )

            await ctx.send(
                embed = await Macro.send(f"This guild doesn't have any self assignable roles")
            )

    @roleme.command(pass_context = True, name = "allow")
    @commands.has_permissions(manage_roles = True)
    async def rollme_allow(self, ctx, *roles: typing.Union[discord.Role]):
        """
        Used to allow users to assign themselves given roles.
        `roleme allow <roles>`
        """
        await ctx.bot.add_self_roles(ctx, *roles)

        await ctx.send(
            embed = await Macro.send(f"Allowed the self roles {', '.join([str(role) for role in roles])}")
        )

    @roleme.command(pass_context = True, name = "deny", aliases = ["block", "disallow"])
    @commands.has_permissions(manage_roles = True)
    async def disallow_self_role(self, ctx, *roles: typing.Union[discord.Role]):
        """
        Used to prevent users from assigning themselves given roles.
        `-roleme disallow <roles>`
        """
        await ctx.bot.remove_self_roles(ctx, *roles)

        await ctx.send(
            embed = await Macro.send(f"Disallowed the self roles {', '.join([str(role) for role in roles])}")
        )

    @roleme.command(pass_context = True, name = "add", aliases = ["set"])
    async def role_add_self(self, ctx, *roles: typing.Union[discord.Role]):
        """
        Used to let users assign themselves allowed roles.
        If acceptable roles are passed in, the caller will be assigned these roles.
        `-roleme self <roles>`
        """
        if len(roles) is 0:
            raise commands.MissingRequiredArgument(discord.Role)

        valid = [role for role in roles if role.id in ctx.bot.cache[str(ctx.guild.id)]["self_roles"]]

        if len(valid) is 0:
            raise Tools.NoValidSelfRoles

        await ctx.author.add_roles(*valid)
        valid = map(str, valid)

        await ctx.send(
            embed = await Macro.send(f"Gave you the roles {', '.join(valid)}")
        )

    @roleme.command(pass_context = True, name = "remove", aliases = ["unset"])
    async def role_remove_self(self, ctx, *roles: typing.Union[discord.Role]):
        """
        Used to let users unassign themselves allowed roles.
        If acceptable roles are passed in, the caller will be assigned these roles.
        `-roleme unself <roles>`
        """
        if len(roles) is 0:
            raise commands.MissingRequiredArgument(discord.Role)

        valid = [role for role in roles if role.id in ctx.bot.cache[str(ctx.guild.id)]["self_roles"] and role in ctx.author.roles]

        if len(valid) is 0:
            raise Tools.NoValidSelfRoles

        await ctx.author.remove_roles(*valid)
        valid = map(str, valid)

        await ctx.send(
            embed = await Macro.send(f"Removed from you the roles {', '.join(valid)}")
        )

def setup(bot):
    bot.add_cog(Roleme(bot))
