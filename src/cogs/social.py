import discord, re
from asyncio import CancelledError
from libs import Macro
from libs.Paginate import Paginated
from discord.ext import commands
from ifunny import Client
from ifunny.objects import User


class Feed:
    def __init__(self, ctx, message, feed):
        self.paginator = Paginated(
            bot = ctx.bot,
            message = message,
            member = ctx.author,
            react_map = {"\U000025b6": self.edit_message},
            on_start = self.edit_message)

        self.message = message
        self.feed = feed

    async def edit_message(self):
        await self.message.edit(embed = await Macro.image(
            url = next(self.feed).content_url))


class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context = True,
                    name = "ifunny",
                    aliases = ["if", "iFunny"])
    async def ifunny(self, ctx):
        """
        iFunny command group

        `-iFunny`
        """
        return

    async def user_card(self, user):
        about = re.sub("(\|\||\*\*|\_\_|\*|\`|\`\`\`)",
                       lambda x: f"\\{x.group()}", user.about)

        card = await Macro.send(description = about,
                                title = user.nick,
                                color = discord.Color(int(user.nick_color,
                                                          16)))

        if user.profile_image:
            card.set_thumbnail(url = user.profile_image.url)

        card.add_field(name = "subscribers", value = user.subscriber_count)

        card.add_field(name = "subscriptions", value = user.subscription_count)

        card.add_field(name = "posts", value = user.total_posts)

        card.add_field(name = "features", value = user.total_featured)

        card.add_field(name = "rank",
                       value = f"{user.rank} with {user.days} days active",
                       inline = False)

        card.add_field(
            name = "rating",
            value = f"level {user.rating.level} with {user.rating.points} exp",
            inline = False)

        return card

    @ifunny.command(pass_context = True, name = "user")
    async def ifunny_user(self, ctx, nick, *_):
        message = await ctx.send(embed = await Macro.send(f"Finding {nick}"))
        user = User.by_nick(nick)

        if not user:
            return await message.edit(
                emebd = await Macro.send(f"No such user {nick} on iFunny"))

        card = await self.user_card(user)

        await message.edit(embed = card)

    @ifunny.command(pass_context = True,
                    name = "features",
                    alias = ["featured"])
    async def ifunny_features(self, ctx):
        message = await ctx.send(embed = await Macro.send(f"Getting features"))

        feed = Client().featured
        paginator = Feed(ctx, message, feed)
        try:
            await paginator.paginator.start()
        except CancelledError:
            return

    @ifunny.command(pass_context = True, name = "timeline")
    async def ifunny_user_timeline(self, ctx, nick, *_):
        message = await ctx.send(embed = await Macro.send(f"Finding {nick}"))

        user = User.by_nick(nick)

        if not user:
            return await message.edit(
                embed = await Macro.send(f"No such user {nick} on iFunny"))

        await message.edit(
            embed = await Macro.send(f"Getting {user}'s timeline'"))

        feed = user.timeline
        paginator = Feed(ctx, message, feed)
        try:
            await paginator.paginator.start()
        except CancelledError:
            return


def setup(bot):
    bot.add_cog(Social(bot))
