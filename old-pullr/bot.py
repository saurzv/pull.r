import os
import discord

from dotenv import load_dotenv

from keep_running import keep_running

from utils.get_manual import get_manual
from utils.get_image_data import get_image_data

load_dotenv()

class Bot(discord.Client):
    """ Main bot class """

    async def on_ready(self):
        """ Print message in log after succesful initial run """
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        """ See message, and respond accordingly """
        if message.author == self.user:
            return

        if message.content.startswith('-man'):
            embed = discord.Embed(title='pull.r manual')
            get_manual(embed)
            await message.channel.send(embed=embed)

        if message.content.startswith('-x'):
            img_data = get_image_data(message.content)
            if img_data == -1 :
                await message.channel.send('Not a vaild command, type -man for manual')
                return

            embed = discord.Embed(
                title=img_data[1], description=img_data[2],url=img_data[3])
            embed.set_image(url=img_data[0])
            await message.channel.send(embed=embed)

TOKEN = os.getenv('TOKEN')
bot = Bot()
keep_running()
bot.run(TOKEN)
