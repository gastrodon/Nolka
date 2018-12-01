"""
Cache module for a Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming to readthedocs.io soon
"""

import discord, pickle

def stash(ctx, path = "pickle"):
    print("stashing ", ctx)
    with open(path, "w") as lock:
        pickle.dump(ctx, lock)
