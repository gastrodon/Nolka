#### About

Commands and usage of Nolka, the discord bot

#### Commands

##### `-role give`_`[roles] *[users]`_

Assigns roles to users. If given roles do not exist, they are created as normal roles. If no users are given, roles are just created

-  `roles` : any number of roles. If they're not on the server, they're created
-  `users` : @mention of any number of users on the server

##### `-role take`_`[roles] [users]`_

Takes any number of roles from any number of users

-  `roles` : any number of roles that exist on the server
-  `users` : @mention of any number of users on the server

##### `-role kill`_`[roles]`_

Deletes any number of roles from the server

-  `roles` : any number of roles that exist on the server

##### `-booru search`_`[tags]`_

Queries [Gelbooru](http://gelbooru.com) for an image for given tags

-  `tags` : any number of tags that you would use normally on Gelbooru

##### `-booru dump`_`[tags] *size=10 *begin=random`_

Queries [Gelbooru](http://gelbooru.com) for a list of images for given tags in sequential order by post index

-  `tags` : any number of tags that you would use normally on Gelbooru
-  `size` : how many images to dump, default 10
-  `begin` : post index to begin dumping at, default random
