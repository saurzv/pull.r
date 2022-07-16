import requests
import time

from discord.ext.commands import Cog, command, Context


class Jokes(Cog):

    def __init__(self, client) -> None:
        self.client = client

    @command(
        name='joke',
        brief=': Send a joke, type -help joke for more options',
        help=
        'Available categories(case insensitive) are:\nProgramming, Misc, Dark, Pun, Spooky, Christmas\n\nTry: -joke Programming Dark',
        description='Set categories to narrow down the result.',
    )
    async def joke(self, ctx: Context, *categories: str) -> None:
        category_tags = ''

        if len(categories) > 0:
            for category in categories:
                category_tags += category.title() + ','
            category_tags = category_tags[:-1]
        else:
            category_tags = 'Any'

        api_url = 'https://v2.jokeapi.dev/joke/' + category_tags

        rsp = requests.get(api_url)
        json_data = rsp.json()

        if (json_data['error'] == False):
            if (json_data['type'] == 'single'):
                await ctx.send(json_data['joke'])

            elif (json_data['type'] == 'twopart'):
                await ctx.send(json_data['setup'])
                time.sleep(1.5)
                await ctx.send(json_data['delivery'])

        else:
            await ctx.send(json_data['additionalInfo'].split('Got')[0])


def setup(Client) -> None:
    Client.add_cog(Jokes(Client))