import discord, json, Cache, Messages
import discord.ext.commands as commands

# Globals

Nolka = commands.Bot(command_prefix="+")
with open("token.json") as doc:
    token = json.load(doc)["token"]
Servers = Cache.Server()
embedColor = discord.Color(0x82b1ff)
errorColor = discord.Color(0xff72bb)
colors = {
    "normal": discord.Color(0x82b1ff),
    "error": discord.Color(0xff72bb)
}

# Helper functions

def embedMessage(description, status = "normal", title = None, ctx = None, **kwargs):
    global colors
    if status is not "failedInit":
        color = Servers.color(ctx.message.server, status)
    else:
        color = colors["error"]
    message = discord.Embed(
        type = "rich",
        title = title,
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
    if not ctx.message.author.permissions_in(ctx.message.channel).administrator:
        await Nolka.send_message(
            Servers.get(ctx.message.server, "bot"),
            embed = embedMessage(Messages.noAdmin, status = "error")
        )
        return False
    return True

# Bot events

@Nolka.event
async def on_ready():
    await Nolka.change_presence(game = discord.Game(
        name = "Local Dev",
        type = 1
    ))

# Bot commands

@Nolka.command(pass_context = True)
async def test(ctx, *args):
    await Nolka.send_message(
        Servers.get(ctx.message.server, "bot"),
        embed = embedMessage("Tested")
    )


@Nolka.command(pass_context = True)
async def init(ctx, *args):
    global colors
    if not await admin(ctx):
        return
    if len(args) is 0 or args[0] == "here":
        Servers.initServer(
            ctx.message.server,
            ctx.message.channel,
            colors
        )
        await Nolka.send_message(
            Servers.get(ctx.message.server, "bot"),
            embed = embedMessage(Messages.initMessage, ctx = ctx)
        )
        return
    if args[0] in [channel.name for channel in ctx.message.server.channels]:
        Servers.initServer(
            ctx.message.server,
            [channel for channel in ctx.message.server.channels if channel.name == args[0]][0],
            colors
        )
        await Nolka.send_message(
            Servers.get(ctx.message.server, "bot"),
            embed = embedMessage(Messages.initMessage, ctx = ctx)
        )
        return
    await Nolka.send_message(
        ctx.message.channel,
        embed = embedMessage(Messages.badChannel.format(args[0]), ctx = ctx, status = "failedInit")
    )

@Nolka.command(pass_context = True)
async def color(ctx, *args, type = "normal"):
    global colors
    args = [arg for arg in args]
    if len(args) is 0:
        await Nolka.send_message(
            Servers.get(ctx.message.server, "bot"),
            embed = embedMessage(Messages.missingArgs, ctx = ctx, status = "error")
        )
        return
    if len(args) is 2:
        if args[0] not in colors:
            await Nolka.send_message(
                Servers.get(ctx.message.server, "bot"),
                embed = embedMessage(Messages.colorTypes.format(
                    "- {}\n" * len(colors)
                ).format(
                    *[x for x in colors]
                ), ctx = ctx,
                status = "error")
            )
            return
        type = args.pop(0)
    if colored(args[0]) is -1:
        await Nolka.send_message(
            Servers.get(ctx.message.server, "bot"),
            embed = embedMessage(Messages.badColor.format(args[0]), ctx = ctx, status = "error")
        )
        return
    Servers.setColor(
        ctx.message.server,
        type,
        colored(args[0])
    )
    await Nolka.send_message(
        Servers.get(ctx.message.server, "bot"),
        embed = embedMessage(Messages.colorSet.format(type, args[0]), ctx = ctx)
    )

@Nolka.group(pass_context = True)
async def role(ctx):
    if not await admin(ctx):
        return
    if ctx.invoked_subcommand is None:
        await Nolka.send_message(
            Servers.get(ctx.message.server, "bot"),
            embed = embedMessage(Messages.noSubcommand, status = "error", ctx = ctx)
        )

@role.command(pass_context = True)
async def give(ctx, *args):
    args = [arg.lower() for arg in args if "@" not in arg]
    roles = [role for role in ctx.message.server.roles if str(role).lower() in args]
    print(ctx.message.server)
    for arg in args:
        if arg not in [str(role).lower() for role in ctx.message.server.roles]:
            await Nolka.create_role(ctx.message.server, name = arg)

@role.command(pass_context = True)
async def create(ctx, *args):
    await Nolka.create_role(ctx.message.server, name = "newrole")

# Start the bot

Nolka.run(token)
