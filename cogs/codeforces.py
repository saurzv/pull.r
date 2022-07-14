import requests
import json
import discord
from discord.ext.commands import Cog, command, Context


class Codeforces(Cog):

    def __init__(self, client) -> None:
        self.client = client

    @command(
        name='info',
        brief=': Fetch Codeforces rating for one or more username(s).',
        help='-info user1 user2 : Fetch ratings for user1 and user2 respectively.'
    )
    async def info(self, ctx: Context, *usernames: str) -> None:
        usernames_string = ''.join(f'{username};' for username in usernames)
        if usernames_string == '':
            await ctx.send('No username specified!')
            return

        rsp = requests.get(
            f'https://codeforces.com/api/user.info?handles={usernames_string}')
        json_data = rsp.json() if rsp and rsp.status_code == 200 else None

        if json_data == None:
            await ctx.send('An error occured, check username(s).')
            return

        embed = discord.Embed(title='Codeforces Info')

        for user in json_data['result']:
            get_info = {
                'rating': '',
                'maxRating': '',
                # 'rank': '',
                # 'maxRank': '',
            }

            for key, value in user.items():
                try:
                    if get_info[key] == '':
                        get_info[key] = value
                except KeyError:
                    pass

            embed.add_field(name=user['handle'],
                            value='\n'.join(
                                f'{key}: {value}'
                                for key, value in get_info.items()),
                            inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Codeforces(client))