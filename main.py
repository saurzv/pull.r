import discord
import os

from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()

client = Bot(command_prefix='-')


def load_commands() -> None:
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            extention = file[:-3]
            try:
                client.load_extension(f'cogs.{extention}')
                print(f'loading {extention}')
            except:
                print(f'{extention}')


@client.event
async def on_ready() -> None:
    print(f'Logged in as {client.user.name}')


@client.event
async def on_message(message: discord.message) -> None:
    if message.author == client.user:
        return
    await client.process_commands(message)


if __name__ == '__main__':
    load_commands()

TOKEN = os.getenv('TOKEN')
client.run(TOKEN)