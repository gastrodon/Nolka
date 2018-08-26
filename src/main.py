#!/usr/bin/python3.6

import sys

if (sys.version_info[0] is not 3 or sys.version_info[1] is not 6):
    #raise Exception("Must be python verion 3.6.x")
    pass

import discord, asyncio, json, datetime, objects
import discord.ext.commands as commands

Nolka = commands.Bot(command_prefix="-")

# Globals
token = json.load(open("token.json", "r"))["token"]
env = {}
users = {}
verbose = True

# get type of discord object
# dType(id) returns string
def dType(id):
    if Nolka.get_server(id) is not None:
        return "server"
    if Nolka.get_channel(id) is not None:
        return "channel"
    return "unknown"

def update():
    global env
    with open("env.json", "w") as envJSON:
        json.dump(env, envJSON)
    with open("env.json", "r") as envJSON:
        env = json.load(envJSON)

@Nolka.event
async def on_ready():
    global env
    with open("env.json", "r") as envJSON:
        env = json.load(envJSON)
    await Nolka.change_presence(game=discord.Game(name="Local Dev"))

# message hook
@Nolka.event
async def on_message(message):
    await Nolka.process_commands(message)

# member join
@Nolka.event
async def on_member_join(member):
    global env
    Nolka.send_message(env["intro"], "Welcome, {}".format(member.nick))

# member exit
@Nolka.event
async def on_member_leave(member):
    global env
    Nolka.send_message(env["intro"], "Goodbye, {}".format(member.nick))

# Administrator

# testing function
# -test *[arguments]
@Nolka.command(pass_context=True)
async def test(ctx, *args):
    global env
    print(ctx.message.channel.id)
    pass

# set bot server and default channel
#-init location
@Nolka.command(pass_context = True)
async def init(ctx, *args):
    """
    {servers -> id:
        {users -> id:
            {
                tag ->      string,
                birthday -> UNIX timestamp,
            }
        }
    }
    """
    global env
    dict = {}
    dict["users"] = {}
    dict["channels"] = {}
    if len(args) is 0:
        Nolka.say("I need a channel")
        return
    elif args[0] == "here":
        dict["channels"]["bot"] = ctx.message.channel.id
        await Nolka.say("init to here")
    elif args[0] in [_.name for _ in ctx.message.server.channels]:
        dict["channels"]["bot"] = [_ for _ in ctx.message.server.channels if _.name == args[0]][0].id
        await Nolka.say("init to another channel")
    else:
        await Nolka.say("Can't find the server{}".format(args[0]))
        return
    server = ctx.message.server
    for user in server.members:
        dict["users"][user.id] = {}
        dict["users"][user.id]["tag"] = "{}#{}".format(user.name, user.discriminator)
        dict["users"][user.id]["birthday"] = None
    with open("env.json", "w") as envJSON:
        env[server.id] = dict
        json.dump(env, envJSON)
    with open("env.json", "r") as e:
        env = json.load(e)
    await Nolka.send_message(ctx.message.channel, "Init on server {}".format(server))

# set channel for bot activities
#-set [type] [channel]
# TODO update fast
@Nolka.command(pass_context=True)
async def set(ctx, *args):
    global env
    server = str(ctx.message.server.id)
    bot = Nolka.get_channel(env[server]["channels"]["bot"])
    print(bot.name)
    if len(args)<2:
        await Nolka.send_message(bot, "You're missing some arguments")
        return
    if args[1] == "here":
        env[server]["channels"][args[0]] = ctx.message.channel.id
        update()
        await Nolka.send_message(bot, "Set {} channel here".format(args[0]))
        return
    if args[1] not in [_.name for _ in [_ for _ in Nolka.get_server(server).channels]]:
        await Nolka.send_message(bot, "I don't see the channel {}".format(args[1]))
        return
    env[server]["channels"][args[0]] = [_ for _ in Nolka.get_server(server).channels if _.name == args[1]][0].id
    update()
    await Nolka.send_message(bot, "Set {} channel to {}".format(args[0], args[1]))
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
        await Nolka.say("I need at least one role")
        return
    for member in ctx.message.mentions:
        for role in roles:
            await Nolka.add_roles(member, role)
            await Nolka.say("gave role {} to user {}".format(role, member))
    return

# role take from user
#-role take [roles] [users]
@role.command(pass_context=True)
async def take(ctx, *args):
    global env
    roles = [_ for _ in env["server"].roles if _.name.lower() in [_.lower() for _ in args]]
    if len(roles) is 0:
        await Nolka.say("I need at least one role")
        return
    if len(ctx.message.mentions) is 0:
        await Nolka.say("I need at least one user")
        return
    for member in ctx.message.mentions:
        await Nolka.remove_roles(member, *roles)
    await Nolka.say("took roles")
    return

# role create new role
#-role create [roles] *[users]
@role.command(pass_context=True)
async def create(ctx, *args):
    global env
    make = [_ for _ in args if "@" not in _]
    for role in make:
        if role.lower() in [_.name.lower() for _ in env["server"].roles]:
            await Nolka.say("There's already have a role called {} here".format(role))
        else:
            print(env["server"]); return
            await Nolka.create_role(env["server"], name = role)
            await Nolka.say("created role {}".format(role))
    if len(ctx.message.mentions) is not 0:
        for member in ctx.message.mentions:
            for role in [_ for _ in env["server"].roles if _.name.lower() in make]:
                await Nolka.add_roles(member, role)
                await Nolka.say("gave role {} to user {}".format(role, member))
    return

# role delete role
#-role delete [roles]
@role.command(pass_context=True)
async def delete(ctx, *args):
    global env
    kill = [_ for _ in env["server"].roles if _.name in [k for k in args if "@" not in k]]
    if len(kill) is 0:
        await Nolka.say("Didn't find any roles to delete")
        return
    for role in kill:
        if role.name.lower() not in [_.name.lower() for _ in env["server"].roles]:
            await Nolka.say("There's no role called {}".format(role))
        else:
            await Nolka.delete_role(env["server"], role)
            await Nolka.say("Deleted role {}".format(role))
    return

# User

@Nolka.command(pass_context=True)
async def birthday(ctx, *args):

    pass

Nolka.run(token)
