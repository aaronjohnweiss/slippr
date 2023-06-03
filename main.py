# bot.py
import sys
import os
from multiprocessing import Pool

import discord
from dotenv import load_dotenv

from server import Server
from slippi_profile_parser import get_user_from_tag

if __name__ == '__main__':

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    server_data = None

    @client.event
    async def on_ready():
        for guild in client.guilds:
            print('Opening server ' + guild.name)

            if guild.name == GUILD:
                global server_data
                server_data = Server(guild.name)
                print('Server users: ' + str(server_data.users))
                break

        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        if server_data is None:
            print("No server - exiting")
            sys.exit()

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if str(message.channel) != 'meleechat':
            return

        if message.content == '!standings':
            response = await message.channel.send('Fetching stats...')

            global server_data

            pool = None

            print('Creating thread pool..')
            with Pool(len(server_data.users)) as p:
                pool = p.map(get_user_from_tag, server_data.users.keys())

            print('Cleaning up thread results..')
            for item in pool:
                server_data.users[item.uri_name] = item

            def select_elo(tuple):
                return tuple[1].elo

            results = sorted(server_data.users.items(), key=select_elo, reverse=True)

            standings = 'Current standings: \n'
            for idx, tuple in enumerate(results):
                standings += '> ' + str(idx+1) + '. ' + tuple[1].name + ' - ' + tuple[1].rank + ' (' + tuple[1].elo + ')\n'

            await response.edit(content=standings)

        if message.content.startswith("!add"):
            response = await message.channel.send('Adding user...')
            msg = ''
            try:
                print('Adding user...')
                tag = message.content.split()[1]
                user = get_user_from_tag(tag)
                msg = 'User ' + user.name + ' added to the channel standings.'

                server_data.users[user.uri_name] = user
                server_data.save()
            except:
                msg = 'Failed to add user - did you use a valid Slippi tag?'
            await response.edit(content=msg)

        if message.content.startswith("!delete"):
            response = await message.channel.send('Deleting user...')
            tag = message.content.split()[1]

            msg = ''
            try:
                msg = 'User ' + tag + ' removed from the channel standings.'

                del server_data.users[tag]
                server_data.save()
            except KeyError:
                msg = 'Could not remove user: ' + tag + ' does not exist.'
            await response.edit(content=msg)

        if message.content == '!commands' or message.content == '!help':
            response = 'Available Slippr commands:\n> !add <tag#000> to add a user (no < > brackets)\n> !standings to view current server standings\n> !delete <tag#000> to remove a user (no < > brackets)'
            await message.channel.send(response)


    client.run(TOKEN)
