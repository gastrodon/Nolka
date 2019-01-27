"""
Booru module for a Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming to readthedocs.io soon
"""

import discord, json, os, requests, untangle
from libs.Tools import BooruNoPosts

class PostList:
    """
    Gelbooru post response object.
    """
    def __init__(self, ctx, message, page = 1, tags = []):
        """
        Get a page of posts from gelbooru and store it in this object.

        ctx: discord.Context - context from the command
        page: int - page to start searching at
        """
        self.ctx = ctx
        self.message = message
        self.url = "https://gelbooru.com/index.php"
        self.queryStrings = {
            "page": "dapi",
            "pid" : page,
            "q" : "index",
            "s" : "post",
            "api_key" : ctx.bot.gelbooru_api,
            "user_id" : ctx.bot.gelbooru_id,
            "tags" : " ".join(tags)
        }
        self.index = 0
        self.tags = tags
        self.response = requests.get(self.url, params=self.queryStrings)
        self.parsed = untangle.parse(self.response.text)
        if len(parsed.posts) <= 0:
            raise BooruNoPosts
        self.func_map = {
            ":arrow_backward:" : self.prev_image(),
            ":arrow_forward:" : self.next_image()
        }
        self.edit_message()

    async def image(self):
        return self.parsed.posts.post[self.index]

    async def next_image(self):
        self.index += 1
        await self.edit_message()

    async def prev_image(self):
        self.index -= 1
        await self.edit_message()

    def image_watcher_check(self, reaction, user):
        if user.id != self.ctx.message.author.id or reaction.message.id != self.message.id:
            return False
        return demojize(reaction.emoji) in func_map.keys()

    async def image_watcher(self):
        try:
            reaction, user = await self.ctx.bot.wait_for(
                "reaction_add",
                check = self.image_watcher_check,
                timeout = 120
            )
        except:
            return
        else:
            self.func_map[demojize(reaction.emoji)]()

    async def edit_message(self):
        url = self.parsed.posts.post[self.index]
        self.message.edit(
            embed = await Macro.Embed.image(url)
        )
        self.backgroun_task = self.ctx.bot.loop.create_task(self.image_watcher)
