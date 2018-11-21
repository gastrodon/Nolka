"""
Cache module for a Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming to readthedocs.io soon
"""

class Server():
    """
    Discord bot guild info cache.
    """

    def __init__(self):
        """
        Initialize an instance of the cache object.

        self - class : this object
        """
        self.map = {}

    def bind(self, server, object, bind):
        """
        Bind a keyword to a channel by server.

        self - class : this object
        server - discord.Guild : server where the bind will be active
        object - * : object that will be bound
        bind - string : keyword that will be bound
        """
        if not hasattr(object, "id"):
            raise TypeError("Object has no id")
        self.map[server][bind] = object

    def get(self, server, bind):
        """
        Get an object from a server bind.

        self - class : this object
        server - discord.Guild : server where the bind is active
        bind - string : keyword that is bound

        return - * : object that was bound or None
        """
        if server not in self.map:
            return None
        try:
            return self.map[server][bind]
        except:
            return None

    def delete(self, server, bind):
        """
        Unbind an object from a server.

        self - class : this object
        server - discord.Guild : server where the bind is active
        bind - string : keyword that is bound
        """
        if bind not in self.map[server]:
            raise IndexError
        del self.map[server][bind]

    def initServer(self, server, channel, colors):
        """
        Initialize a server on the map.

        self - class : this object
        server - discord.Guild : server that is being initialized
        channel - discord.TextChannel : channel that will be used by Nolka
        colors - dict : dictionary with message accent colors
        """
        self.map[server] = {
            "bot": channel,
            "color":{
                **colors
            }
        }

    def setColor(self, server, status, color):
        """
        Set color to use for a type.

        self - class : this object
        server - discord.Guild : server where the color is being set
        status - string : color status to bind
        color - discord.Colour : color object that is being bound to a status
        """
        self.map[server]["color"][status] = color

    def color(self, server, status = "normal"):
        """
        Get a color from a status bind.

        self - class : this object
        server - discord.Guild : server where the color is bound
        status - string : color status bind, defaults to normal

        return - discord.Colour : color object that status is bound to
        """
        return self.map[server]["color"][status]

    def colorTypes(self, server):
        """
        Get appropriate color status binds for a server.

        server - discord.Guild : server where the status binds exist

        return - string[] : list of status binds for server
        """
        return [x for x in self.map[server]["color"]]
