### Paginate.py (In progress)

Docs for using Paginate.py in your own project. This class works primarily by binding unicode strings (`"U\xxxxxxxx"`) representing emojis to methods to call when that emoji is used in a reaction. The class also has a few other bindable methods to call at specific places, including `on_start`, `on_close`, and `on_error`.

#### External Dependancies
 - [discordpy rewrite](https://github.com/Rapptz/discord.py/tree/rewrite)

#### Other Requirements:

The bot must be in a server in which it has the `manage_messages` permission. This is because that permission is required to clear reactions on it's own message from other users, ie the caller of a command in which pagination is used. It is also recommend to have a fallback or check done before you try to paginate ~~even though I don't do this with my bot~~.

#### Arguments

The `Paginated` class requires a few arguments

 - `bot: discord.Client` This is the bot that will be doing the pagination, and who will be calling background tasks to listen

 - `message: discord.Message` This is the message that will paginate. This should be a message that your bot has authored.

 - `member: discord.User | set/list/tuple | int` This is the user that is allowed to paginate the message.

 - `react_map: dict{string: coroutine}` This is an association map between unicode strings representing reaction emojis and coroutines. String keys in this map will be added by the bot as reactions for ease of clicking. When a reaction is added by a member part of the `member` argument that matches a react in this map, the associated function is fired and the reaction is reset.

 The `Paginated` class also has a few optional keyword arguments.

  - `timeout: int/float` Time to listen for a reaction. If nothing is supplied, this defaults to 60 seconds.

  - `on_start: coroutine` This is called when the `Paginated.start()` class is called. This is useful for when the pagination is started outside of the object or other context that uses it, ie from a command method.

  - `on_close: coroutine` Similar to `on_start`, this is called when the Pagination session is closed for any reason. This is useful in cases where you might delete a message that is no longer being used.

  - `on_error: coroutine` This method is called when some errors are encountered, with a single argument containing the error. If nothing is supplied, the error will be raised instead.

#### Examples

Here is an example of a help class interfacing with `Paginated`

```python
class HelpPaginator:
    def __init__(self, ctx, message):
        self.paginator = Paginated(
            bot = ctx.bot,                  # There should be a context object passed in when creating the parent class
            message = message,              # There should be a message object passed in when creating the parent class
            member = ctx.author,            # The message author is only allowed to change pages
            react_map = {
                "\U000025c0": self.prev,    # left arrow emoji
                "\U000025b6": self.next     # right arrow emoji
            }
            on_start = self.edit_message    # Edit the message with new content when the pagination is ready to start
        )

        self.message = message
        self.page = 0
        self.content = self.get_content()

    async def get_content(self):
        # do something to get content for the next message
        return content

    async def next(self):
        self.page += 1
        self.content = self.get_content()
        await self.edit_message()

    async def prev(self):           
        self.page -= 1
        self.content = self.get_content()
        await self.edit_message()

    async def edit_message(self):
        await self.message.edit(
            self.content
        )

@bot.commands(pass_context = True)
async def help(ctx):
    message = await ctx.send(
        embed = discord.Embed(
            type = "rich",
            description = "getting help..."
        )
    )

    helper = HelpPaginator(ctx, message)    # Give the object the command context, and the message to edit
    await helper.paginator.start()          # Start the pagination
```

And that's it. When the paginator is started, you do not need to worry about managing any of the listeners, background tasks, or messages. This is all done automatically.

#### Getting help

Of course if something shows unexpected behaviors or there is a bug in the class, feel free to [open an issue](https://github.com/basswaver/Nolka/issues/new) or contact me directly via discord in [my server](https://discord.gg/h3ZnhRM).
