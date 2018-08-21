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
    Nolka.change_presence(game=discord.Game(name="Working", url=""))

@Nolka.event
async def on_message(message):
    await Nolka.process_commands(message)

@Nolka.event
async def on_member_join(member):
    global env
    Nolka.send_message(env["intro"], "Welcome, {}".format(member.nick))

# this is for testing to see what things do
@Nolka.command(pass_context=True)
async def test(ctx, *args):
    return

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
        await Nolka.send_message(env["bot"], "Initialized")
        updateEnv("save")
        return
    elif args[0] not in [_.name for _ in channels]:
        await Nolka.say("Failed to initialize, cannot find channel".format(args[0]))
        updateEnv("save")
        return
    env["bot"] = list(filter(lambda _ : _.name == args[0], channels))[0]
    await Nolka.send_message(env["bot"], "Initialized")
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
        await Nolka.send_message(env["bot"], "No argument passed")
        return
    if location == "here":
        env[type] = ctx.message.channel
        await Nolka.send_message(env["bot"], "This is my home now")
        return
    channels = [_ for _ in env["server"].channels]
    if location not in [_.name for _ in channels]:
        await Nolka.send_message(env["bot"], "Can't find channel {}".format(location))
        return
    env[type] = list(filter(lambda _ : _.name == location, channels))[0]
    await Nolka.send_message(env["bot"], "Set {} channel to {}".format(type, env[type].name))
    return

Nolka.run(token)
