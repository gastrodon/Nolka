#!/usr/bin/python3.6

import sys

if (sys.version_info[0] is not 3 or sys.version_info[1] is not 6):
    raise Exception("Must be python verion 3.6.x")

import discord, asyncio, json
import discord.ext.commands as commands
import discord.voice_client as voice

Nolka = commands.Bot(command_prefix="-")

# Globals
token = json.load(open("token.json", "r"))["token"]
env = {}
verbose = True
