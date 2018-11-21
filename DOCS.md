## About

Commands and usage of Nolka, the discord bot

## Commands

`-init`_`*[channel], *here`_

Initialize Nolka on the server

- `no params` or `here` : initialize in the current channel
- `channel` : initialize in a channel, given its name. If channel does not exist, the command fails


`-color`_`*[status = message] [color]`_

Change the normal message accent color

- `status` : type of message to affect, default being normal messages
- `color` : a hexadecimal value for an RGB color

`-role give`_`[roles] *[users]`_

Assigns roles to users. If given roles do not exist, they are created as normal roles. If no users are given, roles are just created

- `roles` : any number of roles. If they're not on the server, they're created
- `users` : @mention of any number of users on the server

`-role take`_`[roles] [users]`_

Takes any number of roles from any number of users

- `roles` : any number of roles that exist on the server
- `users` : @mention of any number of users on the server

`-role kill`_`[roles]`_

Deletes any number of roles from the server

- `roles` : any number of roles that exist on the server
