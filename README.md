[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8ae88459351e4f31ada0174126a72b48)](https://www.codacy.com/app/basswaver/Nolka?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=basswaver/Nolka&amp;utm_campaign=Badge_Grade)

#### What is this?

A discord bot named Nolka written in Python

#### Contributors
[Zero](github.com/basswaver)

#### Dependancies

-   [discordpy rewrite](https://github.com/Rapptz/discord.py/tree/rewrite)
-   [requests](https://pypi.org/project/requests2/)
-   [untangle](https://pypi.org/project/untangle/)

#### Getting Started

Setup script coming soon(?)

-   installing dependancies

use pip to install dependancies with `pip -m install -r requirements.txt` in the projects root folder

-   get your access tokens

use `touch src/token.json` to create a token file and format it and format it in the following way
```json
{
    "token": "(your discord bot oauth token)",
    "gelbooruAPI": "(your gelbooru api key)",
    "gelbooruID": "(your gelbooru account id)"
}
```

-   start the bot

After you've done all of that, you should be able to start using Nolka by getting your bot's link and adding it to your server. Check out the [docs](DOCS.md) to learn about the bot's use

If you run into any issues, please [open an issue](https://github.com/basswaver/Nolka/issues/new)
