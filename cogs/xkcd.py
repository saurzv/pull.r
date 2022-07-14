import discord

from discord.ext.commands import Cog, command, Context
from utils.get_image_data import get_image_data


class Xkcd(Cog):

    def __init__(self, client) -> None:
        self.client = client

    @command(name='xkcd',
             brief=': Gets xkcd, type -help xkcd for more.',
             help=f'option\nrandom: Gets a random xkcd.',
             description='Gets front page xkcd if no option is specified.')
    async def xkcd(self, ctx: Context, option: str = ''):

        link = ''

        if option == '':
            link = 'https://xkcd.com'
        elif option == 'random':
            link = 'https://c.xkcd.com/random/comic/'
        else:
            await ctx.send('Invalid command, type help for command list')
            return

        image_data = get_image_data(link)
        embed = discord.Embed(title=image_data[1],
                              description=image_data[2],
                              url=image_data[3])
        embed.set_image(url=image_data[0])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Xkcd(client))