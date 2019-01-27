"""
Messages module for a Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming to readthedocs.io soon
"""

# Error messages
MissingRequiredArgument = "I'm missing some arguments"
BadArgument = "Those arguments don't work"
MissingPermissions = "You don't have permission to do that"
UserInputError = "Theres a problem with that command"
Forbidden = "I'm not allowed to do that"
CacheReadError = "The cache was not readable, perms need to be reset"
traceback = "Autoreported from guild {} at {}\nMessage: {}\nException in command {}\n{} {}\n\n{}"

# Role messages
rolesMade = "Created the roles {}"
rolesGiven = "Gave the users {} the roles {}"
rolesTaken = "The users {} no longer have the roles {}"
rolesKilled = "Killed the roles {}"
rolesRemoved = "Removed the roles {}"
noRoles = "I can't find any roles"
noMembers = "I can't find any users"

# Infraction commands
goodbye = "Goodbye {}"
muted = "Muted {}"
unmuted = "Unmuted {}"

# Private messages
banned = "You were banned from the server {}\n{}"
reasonGiven = "Reason given: {}"
noReason = "No reason was given"
dmsClosed = "DM's for {} are closed"
removedGeneric = "You have been {} from the server {}\nReason given: {}"

# Invite messages
inviteMessage = "Add me to your server [here]({})"

# Admin Messages
modCreate = "{} is part of the ModSquad"
modRemove = "{} is goen from the ModSquad"

# Cogs messages
cogsLoaded = "Loaded the cogs {}"
cogsUnloaded = "Unloaded the cogs {}"
cogsNotLoaded = "Failed loading the cogs {}"
cogsNotUnloaded = "Failed unloading the cogs {}"
cogsReloaded = "Reloaded the cogs {}"

# Booru messages
booruSearching = "Searching..."

# Utils commands
pingms = "{:.1f}ms"
helpTemplate = "Help"
helpItem = "`{}`: {}"
noDocstring = "No docstring"
