"""
Booru module for a Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming to readthedocs.io soon
"""
import discord, json, os, requests, untangle
from random import randrange

class PostList:
    """
    Gelbooru post response object.
    """
    def __init__(self, *args):
        """
        Get a page of posts from gelbooru and store it in this object.

        self - class : this object
        *args - string[] : tags to query
        """
        with open(os.path.dirname(os.path.realpath(__file__))+"/token.json") as doc:
            stream = json.load(doc)
            api = stream["gelbooruAPI"]
            id = stream["gelbooruID"]
        self.url = "https://gelbooru.com/index.php"
        self.queryStrings = {
            "page": "dapi",
            "q": "index",
            "s": "post",
            "api_key": api,
            "tags": "".join(["{} ".format(tag) for tag in args]),
            "user_id": id
        }
        self.tags = args
        self.response = requests.get(self.url, params=self.queryStrings)
        self.parsed = untangle.parse(self.response.text)

    class Image:
        """
        Parsed image used for the embedMessage macro for Discord.
        """
        def __init__(self, url, meta):
            """
            Create the image

            self - class : this object
            url - string : url to the image
            meta - dict : image metadata
            """
            self.meta = meta
            self.url = url
    def single(self, index = 0):
        """
        Parse an image for an embed message on Discord.

        self - class : this object
        url - string : url to the image
        index - int : index of the image in the response posts, default is 0

        return - PostList.Image : a parsed Image object
        """
        if len(self.parsed.posts) <= 0:
            return None
        itemizedImage = self.Image(
            url = self.parsed.posts.post[index]["file_url"],
            meta = {
                "source": self.parsed.posts.post[index]["source"].split(" ")[0],
                "rating": self.parsed.posts.post[index]["rating"]
            }
        )
        return itemizedImage

    def random(self):
        """
        Get a random image from the response

        self - class : this object
        return - Image : parse image from method single()
        """
        if len(self.parsed.posts) <= 0:
            return None
        return self.single(randrange(len(self.parsed.posts)))

    def dump(self, size):
        """
        Get a range of random images from the response

        self - class : this object
        return - array[Image] | None : list of parsed images from method single(), or None
        """
        if len(self.parsed.posts) <= 0:
            return None
        size = min([size, len(self.parsed.posts) - 1])
        return [self.single(randrange(len(self.parsed.posts) - 1)) for _ in range(size)]

    def dumpSequential(self, size, begin):
        """
        Get a range of sequential images from the response

        self - class : this object
        return - array[Image] | None | string : list of parsed images from method single(), error string, or None
        """
        if len(self.parsed.posts) <= 0:
            return None
        if size >= 100:
            return "badSize"
        size = min([size, len(self.parsed.posts) - 1])
        if not begin:
            begin = randrange(100 - size)
        list = []
        return [self.single(index) for index in range(begin, begin + size)]
