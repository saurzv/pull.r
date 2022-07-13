import os
import discord
import requests
import glob

# import io
# import aiohttp

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from keep_running import keep_running

load_dotenv()


class Scrapper:
    """ Scrape the web page for required information """

    def __init__(self, url: str, classid: str):
        self.url = url
        self.classid = classid

    def get_link(self):
        """ Return link for xkcd images """

        image_data = []

        rsp = requests.get(self.url)
        soup = BeautifulSoup(rsp.text, 'html.parser')
        links = soup.findAll('div', class_=self.classid)

        for link in links:
            image_tag = link.findChildren('img')
            if len(image_tag):
                image_data.append('https:'+image_tag[0]["src"])
                image_data.append(image_tag[0]["alt"])
                image_data.append(image_tag[0]["title"])
                return image_data


class Bot(discord.Client):
    """ Main bot class """

    async def on_ready(self):
        """ Print message in log after succesful initial run """

        print(f'Logged in as {self.user}')

    def get_manual(self, embed):
        """ Get manual for every command """

        for file in glob.glob('./man/*'):
            filename = file.split('/')[2]
            with open(file, 'r') as f:
                line = f.read()
                embed.add_field(name=filename, value=line, inline=False)

    async def on_message(self, message):
        """ See message, and respond accordingly """

        if message.author == self.user:
            return

        if message.content.startswith('-man'):
            embed = discord.Embed(title='pull.r manual')
            self._get_manual(embed)
            await message.channel.send(embed=embed)

        if message.content.startswith('-x'):
            img_link = ''

            if(message.content == '-x frontpg'):
                img_link = 'https://xkcd.com'
            elif(message.content == '-x random'):
                img_link = 'https://c.xkcd.com/random/comic/'

            image = Scrapper(img_link, 'box')
            img_data = image.get_link()

            embed = discord.Embed(
                title=img_data[1], description=img_data[2])
            embed.set_image(url=img_data[0])
            await message.channel.send(embed=embed)

            # Extra computatioin needed to send pic with this method.
            """ async with aiohttp.ClientSession() as session:
                async with session.get(img_link) as rsp:
                    buffer = io.BytesIO(await rsp.read())
            await message.channel.send(file=discord.File(buffer, 'test.png'))
            """


TOKEN = os.getenv('TOKEN')
bot = Bot()
keep_running()
bot.run(TOKEN)
