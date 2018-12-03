"""
Booru query for a bot named Nolka
"""

from libs import Macro, BooruAPI, Messages
from discord.ext import commands

class Booru:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True)
    async def booru(self, ctx):
        """
        Group for gelbooru api lookups
        """
        if ctx.invoked_subcommand is None:
            await ctx.channel.send(
                embed = await Macro.Embed.message(Messages.noSubcommand)
            )

    @booru.command(pass_context = True, aliases = ["query", "random"])
    async def search(self, ctx, *args):
        """
        Query gelbooru for a random image from tags.
        Accepts a list of tags, none required
        """
        response = BooruAPI.PostList(*args)
        image = response.random()
        #TODO: if not image
        if image is None:
            await ctx.channel.send(
                embed = await Macro.Embed.error(
                    Messages.noPosts.format(
                        ", ".join(args)
                    )
                )
            )
            return
        if image.meta["source"] == "":
            message = Messages.descNoSource.format(image.meta["rating"].upper)
        else:
            message = Messages.descSingleImage.format(image.meta["rating"].upper(), image.meta["source"])
        await ctx.channel.send(
            embed = await Macro.Embed.image(image.url, description = message)
        )

    @booru.command(pass_context = True)
    async def dump(self, ctx, *args):
        """
        dump a number of images for given tags.
        Accepts a list of tags and arguments, none required
        Arguments follow the format --argument=value
        Arguments with default values:
            size: int = 10
            begin: int = random integer
        """
        #TODO: use arg.pop to trim the list
        tags = [arg for arg in args if arg[0:2] != "--"]
        response = BooruAPI.PostList(*tags)
        mods = {
            "size": 10,
            "begin": None,
        }
        for arg in [[mod.split("=")[0][2:], mod.split("=")[1]] for mod in args if mod[0:2] == "--"]:
            mods[arg[0]] = int(arg[1])
        #TODO: unpack and change the lib to use **kwargs
        images = response.dumpSequential(mods["size"], mods["begin"])
        if images is None:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Message.noPosts.format(", ".join(tags)))
            )
            return
        counter = 0
        max = len(images)
        for image in images:
            counter += 1
            #TODO: use length method
            if image.meta["source"] == "":
                message = Messages.descNoSource.format(image.meta["rating"].upper()) + "\n" + Messages.dumpIndex.format(counter, max)
            else:
                message = Messages.descSingleImage.format(image.meta["rating"].upper(), image.meta["source"]) + "\n" + Messages.dumpIndex.format(counter, max)
            await ctx.channel.send(
                embed = await Macro.Embed.image(image.url, description = message)
            )

def setup(bot):
    bot.add_cog(Booru(bot))
