# bot.py
import sys
import os
from multiprocessing import Pool

import discord
from dotenv import load_dotenv

from message_handler import handle_message
from server import Server
from slippi_profile_parser import get_user_from_tag

if __name__ == '__main__':

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == GUILD:
                break

        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    @client.event
    async def on_message(message):
        await handle_message(client, message)


    client.run(TOKEN)
