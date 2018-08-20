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

@Nolka.event
async def on_ready():
    print("Nolka started")
    return None

@Nolka.event
async def on_message(message):
    global cmdChannel
    await Nolka.process_commands(message)

@Nolka.event
async def on_member_join(member):
    pass

@Nolka.command(pass_context=True)
async def test(ctx, *args):
    await Nolka.say(ctx.message.author.nick)

# set subgroup, expected to tell the bot what channels to use
@Nolka.group(pass_context=True)
async def set(ctx):
    if ctx.invoked_subcommand is None:
        await Nolka.say("Set what?")

# set intro subcommand, expected to set channel for join and leave remarks
@set.command(pass_context=True)
async def intro(ctx, location=None):
    global env
    if location is None:
        await Nolka.say("I need an intro channel ni:regional_indicator_b::regional_indicator_b:er")
    if location is "here":
        env["intro"] = ctx.message.author
        await Nolka.say("I'll do intro in this channel")

Nolka.run(token)
