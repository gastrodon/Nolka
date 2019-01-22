import requests, os
from io import BytesIO
from PIL import Image, ImageOps, ImageDraw

class Tag():
    def __init__(self, user):
        self.user = user
        self.font = os.path.dirname(os.path.realpath("__file__"))+"/font"
        with requests.get(self.user.avatar_url) as stream:
            self.avatar = Image.open(BytesIO(stream.content))

    def maskedAvatar(self, avatar, size = (160, 160)):
        """
        Return a round avatar, with the border being an alpha mask.

        avatar: image - source image
        """

        width, height = avatar.size
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + (width, height), fill = 255)
        output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        return output.resize(size, Image.ANTIALIAS)


    def render(self):
        """
        Returns a tag for a user.
        """
        avatar = self.maskedAvatar(self.avatar)

class User():
    def __init__(self):
        self.avatar_url = "https://cdn.discordapp.com/avatars/134376825190088704/7ae4945b3ed178acca80914d900a0709.png?size=512"

me = User()
