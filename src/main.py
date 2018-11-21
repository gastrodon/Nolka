import discord, json, datetime, Cache, Messages
import discord.ext.commands as commands

# Globals

Nolka = commands.Bot(command_prefix = "+")
with open("token.json") as doc:
    token = json.load(doc)["token"]
Servers = Cache.Server()

def embedMessage(description, ctx, status = "normal", color = discord.Color(0xff72bb), **kwargs):
    if status is not "failedInit":
        color = Servers.color(ctx.guild, status)
    message = discord.Embed(
        type = "rich",
        description = description,
        color = color,
        **kwargs
    )
    return message

def colored(color):
    color = "0x{}".format(color.replace("0x", "").replace("#", "").lower())
    if len(color) is 5:
        color = "0x{}{}{}".format(*[x * 2 for x in color[2:]])
    if not sorted(["0" <= x <= "f" for x in color[2:]])[0]:
        return -1
    return discord.Color(int(color, 16))

async def admin(ctx):
    if not ctx.message.author.permissions_in(ctx.channel).administrator:
        await Servers.get(ctx.guild, "bot").send(
            embed = embedMessage(Messages.noAdmin, ctx, status = "error")
        )
        return False
    return True

# Bot Events

@Nolka.event
async def on_ready():
    await Nolka.change_presence(activity = discord.Game(
        name = datetime.datetime.now().strftime("Online since %B %dth %Y")
    ))

# Bot Commands

@Nolka.command(pass_context = True)
async def init(ctx, *args):
    colors = {
        "normal": discord.Color(0x82b1ff),
        "error": discord.Color(0xff72bb)
    }
    if not await admin(ctx):
        return
    if len(args) is 0 or args[0] == "here":
        Servers.initServer(
            ctx.guild,
            ctx.channel,
            colors
        )
        await Servers.get(ctx.guild, "bot").send(
            embed = embedMessage(Messages.initMessage, ctx)
        )
        return
    if args[0] in [str(channel) for channel in ctx.guild.channels]:
        Servers.initServer(
            ctx.guild,
            [channel for channel in ctx.guild.channels if str(channel) == args[0]][0],
            colors
        )
        await Servers.get(ctx.guild, "bot").send(
            embed = embedMessage(Messages.initMessage, ctx)
        )
        return
    await ctx.channel.send(
        embed = embedMessage(Messages.badChannel.format(args[0]), ctx, status = "failedInit")
    )

@Nolka.command(pass_context = True)
async def color(ctx, *args, type = "normal"):
    args = [*args]
    if len(args) is 0:
        await Servers.get(ctx.guild, "bot").send(
            embed = embedMessage(Messages.missingArgs, ctx, status = "error")
        )
        return
    if len(args) is 2:
        if args[0] not in Servers.colorTypes(ctx.guild):
            await Servers.get(ctx.guild, "bot").send(
                embed = embedMessage(Messages.colorTypes.format(
                    "- {}\n" * len(Servers.colorTypes(ctx.guild))
                ).format(
                    *Servers.colorTypes(ctx.guild)
                ), ctx, status = "error")
            )
            return
        type = args.pop(0)
    if colored(args[0]) is -1:
        await Servers.get(ctx.guild, "bot").send(
            embed = embedMessage(Messages.badColor.format(args[0]), ctx, status = "error")
        )
        return
    Servers.setColor(
        ctx.guild,
        type,
        colored(args[0])
    )
    await Servers.get(ctx.guild, "bot").send(
        embed = embedMessage(Messages.colorSet.format(type, args[0]), ctx)
    )

@Nolka.group(pass_context = True)
async def role(ctx):
    if not await admin(ctx):
        return
    if ctx.invoked_subcommand is None:
        await Servers.get(ctx.guild, "bot").send(
            embed = embedMessage(Messages.noSubcommand, ctx, status = "error")
        )

@role.command(pass_context = True)
async def give(ctx, *args):
    roles = [role for role in ctx.guild.roles if str(role).lower() in [arg.lower() for arg in args]]
    members = [member for member in ctx.guild.members if member.mention in args]
    for arg in args:
        if arg.lower() not in [str(role).lower() for role in roles] and "@" not in arg:
            roles.append(await ctx.guild.create_role(name = arg))
    if len(roles) is 0:
        await Servers.get(ctx.guild, "bot").send(
            embed = embedMessage(Messages.missingArgs, ctx, status = "error")
        )
    if len(members) is 0:
        await Servers.get(ctx.guild, "bot").send(
            embed = embedMessage(Messages.rolesMade.format(
                "{} " * len(roles)
            ).format(
                *[str(role) for role in roles]
            ), ctx)
        )
        return
    for member in members:
        await member.add_roles(*roles)
    await Servers.get(ctx.guild, "bot").send(
        embed = embedMessage(Messages.rolesGiven.format(
            "{} " * len(members) , "{} " * len(roles)
        ).format(
            *[member.name for member in members], *[str(role) for role in roles]
        ), ctx)
    )

@role.command(pass_context = True)
async def take(ctx, *args):
    roles = [role for role in ctx.guild.roles if str(role).lower() in [arg.lower() for arg in args]]
    members = [member for member in ctx.guild.members if member.mention in args]
    print(members)
    print(roles)
    if len(args) is 0:
        await Servers.get(ctx.guild, "bot").send(
            embed = embedMessage(Messages.missingArgs, ctx, status = "error")
        )
        return
    if len(roles) is 0:
        await Servers.get(ctx.guild, "bot").send(
        embed = embedMessage(Messages.noRoles, ctx, status = "error")
        )
        return
    if len(members) is 0:
        await Servers.get(ctx.guild, "bot").send(
            embed = embedMessage(Messages.noMembers, ctx, status = "error")
        )
        return
    for member in members:
        await member.remove_roles(*roles)
    await Servers.get(ctx.guild, "bot").send(
        embed = embedMessage(Messages.rolesTaken.format(
            "{} " * len(members), "{} " * len(roles)
        ).format(
            *[member.name for member in members], *[str(role) for role in roles]
        ), ctx)
    )

@role.command(pass_context = True)
async def kill(ctx, *args):
    roles = [role for role in ctx.guild.roles if str(role).lower() in [arg.lower() for arg in args]]
    if len(roles) is 0:
        await Servers.get(ctx.guild, "bot").send(
            embed = embedMessage(Messages.missingArgs, ctx, status = "error")
        )
        return
    for role in roles:
        await role.delete()
    await Servers.get(ctx.guild, "bot").send(
        embed = embedMessage(
            Messages.rolesKilled.format(
                "{} " * len(roles)
            ).format(
                *[str(role) for role in roles]
            ), ctx
        )
    )

Nolka.run(token)
