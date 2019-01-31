import discord, untangle, requests
from libs import Macro, Paginate
from libs.Tools import BooruNoPosts

class Booru:
    """
    Superclass for *booru response objects
    """
    def __init__(self, ctx, message, tags):
        self.paginator = Paginate.Paginated(
            ctx = ctx,
            message = message,
            member = ctx.author,
            #{point-left, point-right, information-symbol}
            react_map = {
                "\U000025c0": self.prev_image,
                "\U000025b6": self.next_image,
                "\U00002139": self.toggle_info,
                "\U000023f9": self.stop
            },
            on_start = self.edit_message,
            on_error = self.handle
        )
        self.ctx = ctx
        self.message = message
        self.info = False
        self.index = 0
        self.tags = tags
        self.parsed = None
        self.total = 0

    async def prev_image(self):
        self.index = (self.index - 1 + self.total) % self.total

    async def next_image(self):
        self.index = (self.index + 1 + self.total) % self.total

    async def toggle_info(self):
        self.info = not self.info

    async def handle(self, error):
        if isinstance(error, AttributeError):
            return await self.no_posts()
        await self.message.edit(
            embed = await Macro.send("There was an Error")
        )

    async def no_posts(self):
        await self.message.edit(
            embed = await Macro.send("There was an error")
        )

    async def start(self):
        await self.paginator.start()

    async def stop(self):
        await self.paginator.close()

    async def edit_message(self):
        pass

class Gel(Booru):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://gelbooru.com/index.php"
        self.queryStrings = {
            "page": "dapi",
            "pid" : "page",
            "q" : "index",
            "s" : "post",
            "api_key" : self.ctx.bot.gelbooru_api,
            "user_id" : self.ctx.bot.gelbooru_id,
            "tags" : " ".join(self.tags)
        }
        self.parsed = untangle.parse(requests.get(self.url, params = self.queryStrings).text)
        self.total = len(self.parsed.posts)
        if self.total <= 0:
            self.paginator.close()

    async def edit_message(self):
        if self.info:
            tags = self.parsed.posts.post[self.index]["tags"].strip().split(" ")
            await self.message.edit(
                embed = await Macro.send(
                    "{} of {}\n{}".format(
                        self.index + 1,
                        self.total,
                        "\n".join(tags)
                    )
                )
            )
            return
        url = self.parsed.posts.post[self.index]["file_url"]
        await self.message.edit(
            embed = await Macro.Embed.image(
                url,
                description = "{} of {}".format(self.index + 1, self.total)
            )
        )
