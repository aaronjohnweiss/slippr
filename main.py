# bot.py
import os

import discord
from dotenv import load_dotenv

from message_handler import handle_message


if __name__ == '__main__':

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is connected to the following guild:\n')
        for guild in client.guilds:
            print(f'{guild.name} (id: {guild.id})')

    @client.event
    async def on_message(message):
        await handle_message(client, message)

    client.run(TOKEN)
