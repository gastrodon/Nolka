"""
A Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming to readthedocs.io soon
"""
import discord, json, datetime, os, Booru, Messages
import discord.ext.commands as commands

# Globals

Nolka = commands.Bot(command_prefix = "+")

colors = {
    "normal": discord.Color(0x82b1ff),
    "error": discord.Color(0xff72bb)
}

with open(os.path.dirname(os.path.realpath(__file__))+"/token.json") as doc:
    stream = json.load(doc)
    token = stream["token"]
    invite = stream["invite"]

async def embedMessage(description, status = "normal", image = None, **kwargs):
    """
    Macro for formatting embedded messages for Nolka to send.

    description - string : string containing the message body
    status - string : type of color to get, default "normal" for normal message accent colors
    image - Bool | String : url for an image, or None
    """
    global colors
    message = discord.Embed(
        type = "rich",
        description = description,
        color = colors[status],
        **kwargs
    )
    if image:
        message.set_image(
            url = image
        )
    return message

async def admin(ctx):
    """
    Return representation of a context author having admin permissions in a server.

    ctx - context object : context to get message author and channel permissions

    return - boolean
    """
    if not ctx.message.author.permissions_in(ctx.channel).administrator:
        await ctx.channel.send(
            embed = await embedMessage(Messages.noAdmin, status = "error")
        )
        return False
    return True

# Bot Events

@Nolka.event
async def on_ready():
    """
    Change the presence of Nolka when it is ready.
    """
    ftime = [
        datetime.datetime.now().strftime("%B"),
        datetime.datetime.now().strftime("%d"),
        datetime.datetime.now().strftime("%Y")
    ]
    await Nolka.change_presence(activity = discord.Game(
        name = datetime.datetime.now().strftime("Online since %{} %{}th %{}".format(*ftime))
    ))

@Nolka.event
async def on_message(message):
    """
    Process commands, or send an invite link response to a private message.

    message - discord.Message : message object to reference, supplied from a message
    """
    if message.guild is None and message.author != Nolka.user:
        global invite
        await message.channel.send(
            embed = await embedMessage(
                Messages.inviteMessage.format(invite), None
            )
        )
        return
    await Nolka.process_commands(message)
# Bot Commands

@Nolka.group(pass_context = True)
async def role(ctx):
    """
    Command group for manipulating server roles.

    ctx - context object : context to get server info and admin check, supplied from command
    """
    if not await admin(ctx):
        return
    if ctx.invoked_subcommand is None:
        await ctx.channel.send(
            embed = await embedMessage(Messages.noSubcommand, status = "error")
        )

@role.command(pass_context = True)
async def give(ctx, *args):
    """
    Create and/or assign roles to users, as determined by arguments.

    ctx - context object : context to get server info, supplied from command
    *args - string[] : unsorted list of existing roles, new roles, and server members
    """
    roles = [role for role in ctx.guild.roles if str(role).lower() in [arg.lower() for arg in args]]
    members = [member for member in ctx.guild.members if member.mention in args]
    for arg in args:
        if arg.lower() not in [str(role).lower() for role in roles] and "@" not in arg:
            roles.append(await ctx.guild.create_role(name = arg))
    if len(roles) is 0:
        await ctx.channel.send(
            embed = await embedMessage(Messages.missingArgs, status = "error")
        )
    if len(members) is 0:
        await ctx.channel.send(
            embed = await embedMessage(Messages.rolesMade.format(
                "{} " * len(roles)
            ).format(
                *[str(role) for role in roles]
            ))
        )
        return
    for member in members:
        await member.add_roles(*roles)
    await ctx.channel.send(
        embed = await embedMessage(Messages.rolesGiven.format(
            "{} " * len(members) , "{} " * len(roles)
        ).format(
            *[member.name for member in members], *[str(role) for role in roles]
        ))
    )

@role.command(pass_context = True)
async def take(ctx, *args):
    """
    Take roles from users.

    ctx - context object : context to get server info, supplied from command
    *args - string[] : unsorted list of existing roles and users
    """
    roles = [role for role in ctx.guild.roles if str(role).lower() in [arg.lower() for arg in args]]
    members = [member for member in ctx.guild.members if member.mention in args]
    if len(args) is 0:
        await ctx.channel.send(
            embed = await embedMessage(Messages.missingArgs, status = "error")
        )
        return
    if len(roles) is 0:
        await ctx.channel.send(
        embed = await embedMessage(Messages.noRoles, status = "error")
        )
        return
    if len(members) is 0:
        await ctx.channel.send(
            embed = await embedMessage(Messages.noMembers, status = "error")
        )
        return
    for member in members:
        await member.remove_roles(*roles)
    await ctx.channel.send(
        embed = await embedMessage(Messages.rolesTaken.format(
            "{} " * len(members), "{} " * len(roles)
        ).format(
            *[member.name for member in members], *[str(role) for role in roles]
        ))
    )

@role.command(pass_context = True)
async def kill(ctx, *args):
    """
    Delete roles from a server.

    ctx - context object : context to get server info, supplied from command
    *args - string[] : list of existing roles
    """
    roles = [role for role in ctx.guild.roles if str(role).lower() in [arg.lower() for arg in args]]
    if len(roles) is 0:
        await ctx.channel.send(
            embed = await embedMessage(Messages.missingArgs, status = "error")
        )
        return
    for role in roles:
        await role.delete()
    await ctx.channel.send(
        embed = await embedMessage(
            Messages.rolesKilled.format(
                "{} " * len(roles)
            ).format(
                *[str(role) for role in roles]
            )
        )
    )

@Nolka.group(pass_context = True)
async def booru(ctx):
    """
    Command group for querying gelbooru.

    ctx - context object : context to get server info, supplied from command
    """
    if ctx.invoked_subcommand is None:
        await ctx.channel.send(
            embed = await embedMessage(Messages.noSubcommand, status = "error")
        )

@booru.command(pass_context = True)
async def search(ctx, *args):
    """
    Query gelbooru for an image for given tags

    ctx - context object : context to get server info, supplied from command
    *args - string[] : unsorted collection of tags
    """
    response = Booru.PostList(*args)
    image = response.random()
    if image is None:
        await ctx.channel.send(
            embed = await embedMessage(Messages.noPosts.format(
                "".join(["{} ".format(arg) for arg in args])
            ), status = "error")
        )
        return
    if image.meta["source"] == "":
        message = Messages.descNoSource.format(image.meta["rating"].upper())
    else:
        message = Messages.descSingleImage.format(image.meta["rating"].upper(), image.meta["source"])
    await ctx.channel.send(
        embed = await embedMessage(
            message,
            image = image.url
        )
    )

@booru.command(pass_context = True)
async def dump(ctx, *args):
    """
    Dump a number of images for images for given tags

    ctx - context object : context to get server info, supplied from command
    *args - string[] : unsorted collection of tags and arguments
    *args - size - int : number of items to dump, default 10
    *args - begin - int : post index to start dumping, default None
    """
    tags = [arg for arg in args if arg[0] is not "+"]
    response = Booru.PostList(*tags)
    mods = {
        "size": 10,
        "begin": None
    }
    for arg in [[mod.split(":")[0][1:], mod.split("=")[1]] for mod in args if mod[0] is "+"]:
        mods[arg[0]] = int(arg[1])
    images = response.dumpSequential(mods["size"], mods["begin"])
    if images is None:
        await ctx.channel.send(
            embed = await embedMessage(Messages.noPosts.format(
                "".join(["{} ".format(arg) for arg in args])
            ), status = "error")
        )
        return
    if images is "badSize":
        await ctx.channel.send(
            embed = await embedMessage(Messages.largeDump.format(
                mods["size"]
                ), status = "error")
        )
        return
    difference = mods["size"]
    for image in images:
        difference -= 1
        if image.meta["source"] == "":
            message = Messages.descNoSource.format(image.meta["rating"].upper()) + "\n" + Messages.dumpIndex.format(mods["size"] - difference, mods["size"])
        else:
            message = Messages.descSingleImage.format(image.meta["rating"].upper(), image.meta["source"]) + "\n" + Messages.dumpIndex.format(mods["size"] - difference, mods["size"])
        await ctx.channel.send(
            embed = await embedMessage(
                message,
                image = image.url
            )
        )

Nolka.run(token)
