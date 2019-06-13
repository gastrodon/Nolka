import discord
from libs import Macro
from asyncio import sleep

class CustomPermissionError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NoSubcommand(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NoRolesGiven(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NoReactMethod(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BooruNoPosts(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class RolesTooHigh(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NoValidSelfRoles(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NotSFW(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CannotPaginate(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        except discord.errors.Forbidden:
            return

    @staticmethod
    async def _get_mutable_role(ctx):
        guild = ctx.guild

        if await ctx.bot.flag_check(guild):
            await ctx.bot.flag_clear(guild)
            await ctx.bot.send_debug("cleared flag and updated scope for guild {guild.name}")
            return await Workers._update_mute_scope(guild)

        existing = discord.utils.get(guild.roles, name = "muted")
        return existing if existing else await Workers._update_mute_scope(guild)

    @staticmethod
    async def _update_mute_scope(guild):
        try:
            position = guild.me.top_role.position - 1
            existing = discord.utils.get(guild.roles, name = "muted")
            role = existing if existing else await guild.create_role(name = "muted")
            await role.edit(
                position = position,
                reason = "Updating the mutable role"
            )

            for channel in guild.channels:
                try:
                    await channel.set_permissions(
                        role,
                        reason = "Updating the mutable role",
                        send_messages = False,
                        add_reactions = False
                    )
                except discord.errors.NotFound:
                    pass

        except discord.errors.Forbidden:
            role = None

        return role


    @staticmethod
    async def mute_timer(ctx, user, duration):
        role = await Workers._get_mutable_role(ctx)
        await user.add_roles(role)
        await ctx.send(
            embed = await Macro.send(f"Muted {user.name}")
        )

        if not duration:
            return

        await sleep(duration)
        await user.remove_roles(role)

        await ctx.send(
            embed = await Macro.send(f"{user.name} may speak")
        )
