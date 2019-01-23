"""
Admin management for a bot named Nolka
"""

from libs import Tools
import os


"""
Not every check will be implemented, and I will add more as they're needed
"""

def admin(ctx):
    return ctx.message.author.permissions_in(ctx.channel).administrator

def kick_members(ctx):
    return ctx.message.author.permissions_in(ctx.channel).kick_members

def ban_members(ctx):
    return ctx.message.author.permissions_in(ctx.channel).ban_members

def manage_channels(ctx):
    return ctx.message.author.permissions_in(ctx.channel).manage_channels

def manage_guild(ctx):
    return ctx.message.author.permissions_in(ctx.channel).manage_guild

def manage_roles(ctx):
    return ctx.message.author.permissions_in(ctx.channel).manage_roles

def gaggle(ctx):
    if ctx.guild not in custom_permissions.items:
        raise Tools.CustomPermissionError
