<p align="center">
    <a href="github.address">
        <img src="https://raw.githubusercontent.com/shayanheidari01/rubika/master/icon.png" alt="Shadpy" width="128">
    </a>
    <br>
    <b>Shad API Framework for Python</b>
    <br>
    <a href="https://github.com/shayanheidari01/rubika">
        Homepage
    </a>
    •
    <a href="https://github.com/shayanheidari01/rubika/tree/master/docs">
        Documentation
    </a>
    •
    <a href="https://pypi.org/project/rubpy/#history">
        Releases
    </a>
    •
    <a href="https://t.me/rubika_library">
        News
    </a>
</p>

## Rubpy

> Elegant, modern and asynchronous Shad API framework in Python for users and bots

### Async Accounts
```python
from shadpy import Client, filters, utils
from shadpy.types import Updates

bot = Client(name='shadpy')

@bot.on_message_updates()
async def updates(update: Updates):
    print(update)
    await update.reply(utils.Code('hello') + utils.Underline('from') + utils.Bold('shadpy'))

bot.run()
```

**Async Another Example:**
```python
from shadpy import Client
import asyncio

async def main():
    async with Client(name='shadpy') as bot:
        result = await bot.send_message('me', '`hello` __from__ **shadpy**')
        print(result)

asyncio.run(main())
```

### Sync Accounts
```python
from shadpy import Client

bot = Client('shadpy')

@bot.on_message_updates()
def updates(message):
    message.reply('`hello` __from__ **shadpy**')

bot.run()
```

**Sync Another Example:**
```python
from shadpy import Client

with Client(name='shadpy') as client:
    result = client.send_message('me', '`hello` __from__ **shadpy**')
    print(result)
```

**Shadpy** is a modern, elegant and asynchronous framework. It enables you to easily interact with the main Shad API through a user account (custom client) or a bot
identity (bot API alternative) using Python.


### Key Features

- **Ready**: Install Shadpy with pip and start building your applications right away.
- **Easy**: Makes the Shad API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by pycryptodome, a high-performance cryptography library written in C.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Shad's API to execute any official client action and more.

### Installing

``` bash
pip3 install -U shadpy
```