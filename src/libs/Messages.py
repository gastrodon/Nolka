"""
Messages module for a Discord bot named Nolka.

Author : Zero <dakoolstwunn@gmail.com>
DOCS : Coming to readthedocs.io soon
"""

# Error messages
MissingRequiredArgument = "I'm missing some arguments"
BadArgument = "Those arguments don't work"
badChannel = "The channel {} doesn't exist on this server"
noAdmin = "I don't see you on the list"
noSubcommand = "I'm missing a subcommand"
unknownUser = "I don't know who {} is"
UserInputError = "Theres a problem with that command"
Forbidden = "a 403 error was returned: Forbidden"

# Color messages
colorSet = "Set the {} color to {}"
colorTypes = "These are the valid color types\n{}"
badColor = "The color {} isn't a good hexadecimal color"

# Role messages
rolesMade = "Created the roles {}"
rolesGiven = "Gave the users {} the roles {}"
rolesTaken = "Took from the users {} the roles {}"
rolesKilled = "Killed the roles {}"
rolesRemoved = "Removed the roles {}"
noRoles = "I can't find any roles"
noMembers = "I can't find any users"

# Infraction commands
goodbye = "Goodbye {}"

# Private messages
banned = "You were banned from the server {}\n{}"
reasonGiven = "Reason given: {}"
noReason = "No reason was given"
dmsClosed = "DM's for {} are closed"
removedGeneric = "You have been {} from the server {}\nReason given: {}"

# Invite messages
inviteMessage = "Add me to your server [here]({})"

# Cogs messages
cogsLoaded = "Loaded the cogs {}"
cogsUnloaded = "Unloaded the cogs {}"
cogsNotLoaded = "Failed loading the cogs {}"
cogsNotUnloaded = "Failed unloading the cogs {}"
cogsReloaded = "Reloaded the cogs {}"

# Booru messages
descSingleImage = "Rating: {}\n[Source]({})"
descNoSource = "Rating: {}\nNo source provided"
noPosts = "No images found with the tags {}"
dumpIndex = "Image {} of {}"
largeDump = "{} is too many images for me to dump at once"

# Utils commands
pingms = "{:.1f}ms"
helpTemplate = "Help"
helpItem = "`{}`: {}"
noDocstring = "No docstring"
