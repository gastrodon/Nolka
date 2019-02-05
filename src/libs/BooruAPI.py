import untangle, json, requests
from libs import Macro, Paginate
from discord import Embed

class BooruNoPosts(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Booru:
    """
    Superclass for *booru response objects
    """
    def __init__(self, ctx, message, tags):
        self.react_map = {
        "\U000025c0": self.prev_image,
        "\U000025b6": self.next_image,
        "\U00002139": self.toggle_info,
        "\U000023f9": self.stop,
        "\U0000274c": self.delete
        }
        self.paginator = Paginate.Paginated(
            bot = ctx.bot,
            message = message,
            member = ctx.author,
            # point-left, point-right, information-symbol
            react_map = self.react_map,
            on_start = self.edit_message,
            on_error = self.handle
        )
        self.ctx = ctx
        self.message = message
        self.tags = tags
        self.index = 0
        self.total = 0
        self.page = 0
        self.parsed = None
        self.info = False

    async def prev_image(self):
        self.index = (self.index - 1 + self.total) % self.total
        await self.edit_message()

    async def next_image(self):
        self.index = (self.index + 1 + self.total) % self.total
        await self.edit_message()

    async def toggle_info(self):
        self.info = not self.info
        await self.edit_message()

    async def handle(self, error):
        if isinstance(error, AttributeError):
            return await self.no_posts()
        raise error

    async def no_posts(self):
        await self.message.edit(
            embed = await Macro.send("No posts were found")
        )

    async def start(self):
        await self.paginator.start()

    async def stop(self):
        await self.paginator.close()

    async def edit_message(self):
        pass

    async def delete(self):
        await self.message.delete()
        await self.ctx.message.delete()
        await self.stop()

class Gel(Booru):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://gelbooru.com/index.php"
        self.queryStrings = {
            "page": "dapi",
            "pid" : "page",
            "q"   : "index",
            "s"   : "post",
            "api_key" : self.ctx.bot.gelbooru_api,
            "user_id" : self.ctx.bot.gelbooru_id,
            "tags" : " ".join(self.tags),
            "pid" : self.page + 1
        }
        self.response = requests.get(self.url, params = self.queryStrings)
        self.parsed = untangle.parse(self.response.text)
        self.total = len(self.parsed.posts)
        self.page_count = -(-int(self.parsed.posts["count"]) // self.total)

    async def prev_image(self):
        self.index = (self.index - 1 + self.total) % self.total
        await self.edit_message()

    async def next_image(self):
        self.index += 1
        if self.index >= self.total:
            self.index = 0
            self.page = (self.page + 1 + self.page_count) % self.page_count
            self.queryStrings["pid"] = self.page
            self.response = requests.get(self.url, params = self.queryStrings)
            self.parsed = untangle.parse(self.response.text)
            self.total = len(self.parsed.posts)
        await self.edit_message()

    async def edit_message(self):
        try:
            post = self.parsed.posts.post[self.index]
            rating = post["rating"].upper() if post["rating"] else "?"
        except TypeError:
            post = self.parsed.posts.post
            rating = post["rating"].upper() if post["rating"] else "?"
        if self.info:
            tags = [tag.replace("_", "\_") for tag in post["tags"].strip().split(" ")]
            embed = await Macro.send("\n".join(tags))
            embed.title = f"{self.index + 1} of {self.total} results | Page {self.page} | Rating: {rating}"
            return await self.message.edit(
                embed = embed
            )

        url = post["file_url"]
        source = f"[Source]({post['source'].split(' ')[0]})" if post["source"] else "No source"
        embed = await Macro.Embed.image(url)
        embed.title = f"{self.index + 1} of {self.total} results | Page {self.page} | Rating: {rating}"
        embed.description = source
        return await self.message.edit(
            embed = embed
        )

class Derpi(Booru):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://derpibooru.org/search.json"
        self.queryStrings = {
            "q" : ",".join([a.replace("_", " ") for a in self.tags]),
            "page" : self.page + 1,
            "key" : self.ctx.bot.derpibooru_api
        }
        self.response = requests.get(self.url, params = self.queryStrings)
        self.parsed = json.loads(self.response.text)
        self.total = len(self.parsed["search"])
        self.page_count = -(-self.parsed["total"] // self.total)

    async def prev_image(self):
        self.index -= 1
        if self.index < 0:
            self.page = (self.page - 1 + self.page_count) % self.page_count
            self.queryStrings["page"] = self.page + 1
            self.response = requests.get(self.url, params = self.queryStrings)
            self.parsed = json.loads(self.response.text)
            self.total = len(self.parsed["search"])
            self.index = self.total - 1
        await self.edit_message()

    async def next_image(self):
        self.index += 1
        if self.index >= self.total:
            self.index = 0
            self.page = (self.page + 1 + self.page_count) % self.page_count
            self.queryStrings["page"] = self.page + 1
            self.response = requests.get(self.url, params = self.queryStrings)
            self.parsed = json.loads(self.response.text)
            self.total = len(self.parsed["search"])
        await self.edit_message()

    async def edit_message(self):
        post = self.parsed["search"][self.index]
        tags = [t.strip() for t in post["tags"].split(",")]
        try:
            rating = list(filter(lambda x: x in ["explicit", "questionable", "safe"], tags))[0][0].upper()
        except IndexError:
            rating = "?"
        if self.info:
            embed = await Macro.send("\n".join(tags))
            embed.title = f"{self.index + 1} of {self.total} results | Page {self.page + 1} | Rating: {rating}"
            return await self.message.edit(
                embed = embed
            )
        url = f"https:{post['image']}"
        source = f"[Source]({post['source_url'].split(' ')[0]})" if post["source_url"] else "No source"
        embed = await Macro.Embed.image(url)
        embed.title = f"{self.index + 1} of {self.total} results | Page {self.page + 1} | Rating: {rating}"
        embed.description = source
        return await self.message.edit(
            embed = embed
        )

class E621(Booru):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://e621.net/post/index.json"
        self.queryStrings = {
            "tags" : " ".join(self.tags)
        }
        self.headers = {'User-Agent': self.ctx.bot.user_agent}
        self.response = requests.get(self.url, params = self.queryStrings, headers = self.headers)
        self.parsed = json.loads(self.response.text)
        self.total = len(self.parsed)
        self.page_count = None

    async def prev_image(self):
        self.index -= 1
        if self.index < 0:
            if self.page == 0:
                self.index = 0
                return await self.edit_message()
            self.page -= 1
            self.queryStrings["page"] = self.page + 1
            self.response = requests.get(self.url, params = self.queryStrings, headers = self.headers)
            self.parsed = json.loads(self.response.text)
            self.total = len(self.parsed)
            self.index = self.total - 1
        await self.edit_message()

    async def next_image(self):
        self.index += 1
        if self.index >= self.total:
            self.index = 0
            self.page += 1
            self.queryStrings["page"] = self.page + 1
            self.response = request.get(self.url, params = self.queryStrings, headers = self.headers)
            self.parsed = json.loads(self.response.text)
            self.total = len(self.parsed)
        await self.edit_message()

    async def edit_message(self):
        post = self.parsed[self.index]
        tags = post["tags"].split(" ")
        rating = post["rating"].upper()
        if self.info:
            embed = await Macro.send("\n".join(tags))
            embed.title = f"{self.index + 1} of {self.total} results | Page {self.page + 1} | Rating: {rating}"
            return await self.message.edit(
                embed = embed
            )
        url = post["file_url"]
        source = f"[Source]({post['source'].split(' ')[0]})"  if post['source'] else "No source"
        embed = await Macro.Embed.image(url)
        embed.title = f"{self.index + 1} of {self.total} results | Page {self.page + 1} | Rating: {rating}"
        embed.description = source
        return await self.message.edit(
            embed = embed
        )
