"""
Server management for a bot named Nolka
"""

from libs import Macro, Messages
from discord.ext import commands

class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True)
    async def role(self, ctx):
        """
        Group for manipulating guild roles.
        """
        if ctx.invoked_subcommand is None:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.noSubcommand)
            )

    @role.command(pass_context = True, aliases = ["create", "new"])
    @commands.check(Macro.admin)
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

    @role.command(pass_context = True)
    @commands.check(Macro.admin)
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

    @role.command(pass_context = True, aliases = ["remove", "delete"])
    @commands.check(Macro.admin)
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

def setup(bot):
    bot.add_cog(Admin(bot))
