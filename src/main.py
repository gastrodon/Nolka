#!/usr/bin/python3.6

import sys

if (sys.version_info[0] is not 3 or sys.version_info[1] is not 6):
    raise Exception("Must be python verion 3.6.x")

import discord, asyncio, json
import discord.ext.commands as commands

Nolka = commands.Bot(command_prefix="-")

# Globals
token = json.load(open("token.json", "r"))["token"]
env = json.load(open("env.json", "r"))


try:
    server = env["server"]
except KeyError:
    server = None

# TODO json can't save objects, find a different way to save and load channel and server info
def updateEnv():
    global env
    try:
        with open("env.json", "w") as out:
            json.dump(env, out)
            out.close()
        env = json.load(open("env.json", "r"))
    except:
        raise Exception("Problem saving env to json")
    return

@Nolka.event
async def on_ready():
    await Nolka.change_presence(game=discord.Game(name="under construction"))
    return

@Nolka.event
async def on_message(message):
    await Nolka.process_commands(message)

@Nolka.event
async def on_member_join(member):
    global env
    await Nolka.send_message(env[member.server.id]["intro"])

# this is for testing to see what things do
@Nolka.command(pass_context=True)
async def test(ctx, *args):
    await Nolka.say(ctx.message.content)

# set bot server and default channel
#-init location
@Nolka.command(pass_context=True)
async def init(ctx, *args):
    print("init start")
    global server
    global env
    env["server"] = ctx.message.server
    channels = [_ for _ in env["server"].channels]
    if len(args) is 0:
        await Nolka.say("Failed to initialize, no channel given")
        return
    if args[0] == "here":
        env["bot"] = ctx.message.channel
        updateEnv()
        await Nolka.send_message(Nolka.get_channel(env["bot"]), "Initialized")
        print("init done")
        return
    elif args[0] not in [_.name for _ in channels]:
        await Nolka.say("Failed to initialize, cannot find channel".format(args[0]))
        return
    env["bot"] = list(filter(lambda _ : _.name == args[0], channels))[0]
    updateEnv()
    await Nolka.send_message(Nolka.get_channel(env["bot"]), "Initialized")
    print("init done")

# set channel for bot activities
#-set type channel
@Nolka.command(pass_context=True)
async def set(ctx, *args):
    type = args[0]
    location = args[1]
    global env
    if location is None:
        await Nolka.send_message(Nolka.get_channel(env["bot"].id), "No argument passed")
        return
    if location is "here":
        env[type] = ctx.message.channel
        await Nolka.send_message(Nolka.get_channel(env["bot"].id), "This is my home now")
        updateEnv()
        return
    channels = [_ for _ in server.channels]
    if location not in channels:
        await Nolka.send_message(get_channel(env["bot"].id), "Can't find channel {}".format(location))
        return
    env[type] = list(filter(lambda _ : _.name == location, channels))[0]
    Nolka.send_message(get_channel(env["bot"].id), "Set home channel to {}".format(env[type].name))
    return

Nolka.run(token)
