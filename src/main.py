#!/usr/bin/python3.6

import sys

if (sys.version_info[0] is not 3 or sys.version_info[1] is not 6):
    raise Exception("Must be python verion 3.6.x")

import discord, asyncio, json
import discord.ext.commands as commands

Nolka = commands.Bot(command_prefix="-")

# Globals
token = json.load(open("token.json", "r"))["token"]
env = {}
verbose = True

# shorthand for Nolka.send_message() to bot channel
async def say(message):
    global env
    await Nolka.send_message(env["bot"], message)
    return

# for verbose output
async def log(message):
    global env
    if verbose:
        await Nolka.send_message(env["bot"], message)
    return

# get type of discord object
# dType(id) returns string
def dType(id):
    if Nolka.get_server(id) is not None:
        return "server"
    if Nolka.get_channel(id) is not None:
        return "channel"
    return "unknown"

# TODO Looks like save works, build loading part
def updateEnv(type):
    global env
    if type is "load":
        try:
            source = json.load(open("env.json"))
        except:
            raise Exception("didn't open file")
        for obj in source:
            if source[obj]["type"] == "server":
                env["server"] = Nolka.get_server(source[obj]["id"])
            if source[obj]["type"] == "channel":
                env[obj] = Nolka.get_channel(source[obj]["id"])
        return
    if type is "save":
        formatted = {}
        for obj in env:
            try:
                formatted[obj] = {}
                formatted[obj]["id"] = env[obj].id
                formatted[obj]["type"] = dType(formatted[obj]["id"])
            except:
                raise Exception("can't create formatted json with object {} called {}".format(obj.id, obj.name))
        with open("env.json", "w") as out:
            json.dump(formatted, out)
            out.close()
        updateEnv("load")
        return

# TODO load env.json when bot connects
@Nolka.event
async def on_ready():
    updateEnv("load")
    await Nolka.change_presence(game=discord.Game(name="Working"))

# message hook
@Nolka.event
async def on_message(message):
    await Nolka.process_commands(message)

# member join message
@Nolka.event
async def on_member_join(member):
    global env
    Nolka.send_message(env["log"], "Welcome, {}".format(member.nick))

# member exit message
@Nolka.event
async def on_member_leave(member):
    global env
    Nolka.send_message(env["log"], "Goodbye, {}".format(member.nick))

@Nolka.command()
async def verbose(*args):
    global verbose
    try:
        if args[0] is "1" or args[0] is "True":
            verbose = True
            return
        if args[0] is "0" or args[0] is "False":
            verbose = False
            return
    except:
        verbose = not Verbose
        return
    finally:
        await say("Supply a boolan, or toggle")

# testing function
# -test arguments (if any)
@Nolka.command(pass_context=True)
async def test(ctx, *args):
    global env
    print(ctx.message.mentions)
    for user in ctx.message.mentions:
        print(user)

# set bot server and default channel
#-init location
@Nolka.command(pass_context=True)
async def init(ctx, *args):
    global env
    env["server"] = ctx.message.server
    channels = [_ for _ in env["server"].channels]
    if len(args) is 0:
        await Nolka.say("Failed to initialize, no channel given")
        updateEnv("save")
        return
    if args[0] == "here":
        env["bot"] = ctx.message.channel
        await say("Initialized")
        updateEnv("save")
        return
    elif args[0] not in [_.name for _ in channels]:
        await Nolka.say("Failed to initialize, cannot find channel".format(args[0]))
        updateEnv("save")
        return
    env["bot"] = [_ for _ in channels if _.name == args[0]][0]
    await say("Initialized")
    updateEnv("save")

# set channel for bot activities
#-set type channel
@Nolka.command(pass_context=True)
async def set(ctx, *args):
    type = args[0]
    location = args[1]
    global env
    server = env["server"]
    if location is None:
        await say("No argument passed")
        return
    if location == "here":
        env[type] = ctx.message.channel
        await say("This is my home now")
        return
    channels = [_ for _ in env["server"].channels]
    if location not in [_.name for _ in channels]:
        await say("Can't find the channel {}".format(location))
        return
    env[type] = list(filter(lambda _ : _.name == location, channels))[0]
    await say("Set channel {} to {}".format(type, env[type].name))
    return

# role manipulaiton group
@Nolka.group(pass_context=True)
async def role(ctx):
    if ctx.invoked_subcommand is None:
        pass

# role give to user
# -role add role user
@role.command(pass_context=True)
async def give(ctx, *args):
    global env
    roles = [_ for _ in env["server"].roles if _.name.lower() in [_.lower() for _ in args]]
    if len(roles) is 0:
        await say("I need at least one role")
        return
    for member in ctx.message.mentions:
        for role in roles:
            await Nolka.add_roles(member, role)
            await log("gave role {} to user {}".format(role, member))
    return

# role take from user
# -role take role user
@role.command(pass_context=True)
async def take(ctx, *args):
    global env
    roles = [_ for _ in env["server"].roles if _.name.lower() in [_.lower() for _ in args]]
    if len(roles) is 0:
        await say("I need at least one role")
        return
    for member in ctx.message.mentions:
        for role in roles:
            await Nolka.remove_roles(member, role)
            await log("took role {} from user {}".format(role, member))
    return

@role.command(pass_context=True)
async def create(ctx, *args):
    global env
    make = [_ for _ in args if "@" not in _]
    for role in make:
        if role.lower() in [_.name.lower() for _ in env["server"].roles]:
            await say("There's already have a role called {} here".format(role))
        else:
            await Nolka.create_role(env["server"], name = role)
            await log("created role {}".format(role))
    if len(ctx.message.mentions) is not 0:
        for member in ctx.message.mentions:
            for role in [_ for _ in env["server"].roles if _.name.lower() in make]:
                await Nolka.add_roles(member, role)
                await log("gave role {} to user {}".format(role, member))
    return

#
@role.command(pass_context=True)
async def delete(ctx, *args):
    global env
    kill = [_ for _ in env["server"].roles if _.name in [k for k in args if "@" not in k]]
    if len(kill) is 0:
        await log("Didn't find any roles to delete")
        return
    for role in kill:
        if role.name.lower() not in [_.name.lower() for _ in env["server"].roles]:
            await say("There's no role called {}".format(role))
        else:
            await Nolka.delete_role(env["server"], role)
            await log("Deleted role {}".format(role))
    return

Nolka.run(token)
