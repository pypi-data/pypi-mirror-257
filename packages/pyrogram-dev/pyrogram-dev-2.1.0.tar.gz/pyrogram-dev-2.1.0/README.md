<p align="center">
    <a href="https://github.com/pyrogram-dev/pyrogram-dev">
        <img src="https://graph.org/file/0fef218ce9414e4115c3d.png" alt="Pyrogram-Dev" width="128">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://github.com/AdityaHalder/pyrogram-dev">
        Homepage
    </a>
    •
    <a href="https://docs.pyrogram.org">
        Documentation
    </a>
    •
    <a href="https://github.com/AdityaHalder/pyrogram-dev/releases/latest">
        Releases
    </a>
    •
    <a href="https://t.me/AdityaServer">
        News
    </a>
</p>

## Pyrogram-Dev

> A fork version elegant, modern and asynchronous Telegram MTProto API framework of [Pyrogram](https://github.com/pyrogram/pyrogram) library in Python for users and bots.


``` python
from pyrogram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from Pyrogram-Dev!")


app.run()
```

**Pyrogram-Dev** is a modern, elegant and asynchronous [MTProto API](https://github.com/pyrogram-dev/pyrogram-dev)
framework. It enables you to easily interact with the main Telegram API through a user account (custom client) or a bot
identity (bot API alternative) using Python.


### Key Features

- **Ready**: Install Pyrogram-Dev with pip and start building your applications right away.
- **Easy**: Makes the Telegram API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by [TgCrypto](https://github.com/pyrogram/tgcrypto), a high-performance cryptography library written in C.  
- **Type-hinted**: Types and methods are all type-hinted, enabling excellent editor support.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Telegram's API to execute any official client action and more.

### Installing

``` bash
pip3 install --force-reinstall pyrogram-dev
```

### Resources

- Join our official [**`telegram channel`**](https://t.me/adityaserver) and stay tuned for news, updates and announcements.


### Special Thanks

- [Pyrogram](https://github.com/pyrogram/pyrogram) - Pyrogram is a original library source from which pyrogram-dev was built.


