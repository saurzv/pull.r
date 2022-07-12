import os
import discord
import io
import aiohttp
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

class Scrapper:

    def __init__(self, url: str, classid: str):
        self.url = url
        self.classid = classid

    def get_link(self) -> str:
        rsp = requests.get(self.url)
        soup = BeautifulSoup(rsp.text, 'html.parser')
        links = soup.findAll('div', class_=self.classid)

        for link in links:
            image_tag = link.findChildren('img')
            if len(image_tag):
                return 'https:'+image_tag[0]["src"]

class Bot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('-r.greet'):
            await message.channel.send(f'Hello {message.author}')

        if message.content.startswith('-x'):
            img_link=''
            if(message.content == '-x.today') :
                image = Scrapper('https://xkcd.com', 'box')
                img_link = image.get_link()
            elif(message.content == '-x.random') :
                image = Scrapper('https://c.xkcd.com/random/comic/', 'box')
                img_link = image.get_link()
                
            async with aiohttp.ClientSession() as session:
                async with session.get(img_link) as rsp:
                    buffer = io.BytesIO(await rsp.read())
            await message.channel.send(file=discord.File(buffer, 'test.png'))



TOKEN =os.getenv('TOKEN')
bot = Bot()
bot.run(TOKEN)
