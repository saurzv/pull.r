import os
import asyncio
import requests
import discord

from dotenv import load_dotenv
from discord.ext.commands import command, Cog, Context

load_dotenv()

url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

xRapidAPIKey = os.getenv('X-RapidAPI-Key')
xRapidAPIHost = os.getenv('X-RapidAPI-Host')

headers = {"X-RapidAPI-Key": xRapidAPIKey, "X-RapidAPI-Host": xRapidAPIHost}


class Dictionary(Cog):

    def __init__(self, client) -> None:
        self.client = client

    @command(
        name='define',
        brief=
        ': Definition from the Urban Dictionary. Type -help define for more info.',
        description=
        'Use the arrow key to move between pages, press X after you are done with moving (important for best performance)',
        help='e.g\n-define Bruh: get definition for the word "Bruh"')
    async def define(self, ctx: Context, *keywords: str) -> None:
        querystring = ''
        if len(keywords) > 1:
            for keyword in keywords:
                querystring += keyword + ' '
        else:
            querystring = keywords[0]

        query = {'term': querystring}

        rsp = requests.request("GET", url=url, headers=headers, params=query)

        current = 0
        pages = []
        n = 0

        buttons = [u"\u23EA", u"\u25C0", u"\u25B6", u"\u23E9", u"\u274E"]

        for item in rsp.json()['list']:
            embed = discord.Embed(title=querystring.title(),
                                  description=item['definition'])
            embed.add_field(name='Example', value=item['example'])
            embed.set_footer(text=f'page: {n+1}/{10}')
            n += 1
            pages.append(embed)

        message = await ctx.send(embed=pages[current])

        for button in buttons:
            await message.add_reaction(button)

        while True:

            try:
                reaction, user = await self.client.wait_for(
                    'reaction_add',
                    timeout=40.0,
                    check=lambda reaction, user: user == ctx.author)

            except asyncio.TimeoutError:
                await message.clear_reactions()
                break

            else:
                if reaction.emoji == u"\u274E":
                    await message.clear_reactions()
                    break

                previous = current

                if reaction.emoji == u"\u23EA":
                    current = 0
                elif reaction.emoji == u"\u25C0":
                    if current > 0:
                        current -= 1
                elif reaction.emoji == u"\u25B6":
                    if current < n - 1:
                        current += 1
                elif reaction.emoji == u"\u23E9":
                    current = n - 1

                for button in buttons:
                    await message.remove_reaction(button, user)

                if previous != current:
                    await message.edit(embed=pages[current])


def setup(client):
    client.add_cog(Dictionary(client))