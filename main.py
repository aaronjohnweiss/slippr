# bot.py
import os
import discord
from server import Server
from dotenv import load_dotenv
from message_handler import handle_message
from discord.ext import tasks

if __name__ == '__main__':

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')
    print(GUILD)
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is connected to the following guild:\n')
        for guild in client.guilds:
            print(f'{guild.name} (id: {guild.id})')
        scheduled_countdown.start()

    @client.event
    async def on_message(message):
        await handle_message(client, message)


    @tasks.loop(hours=1)
    async def scheduled_countdown():
        for guild in client.guilds:

            server_data = Server(guild.name)
            if not hasattr(server_data, 'countdown'):
                continue
            if server_data.countdown.active:
                did_decrement = server_data.countdown.decrement()
                if not did_decrement:
                    continue

                server_data.save()

                meleechat = next(obj for obj in guild.channels if obj.name == 'meleechat')

                msg = server_data.countdown.status()

                channel = client.get_channel(meleechat.id)
                await channel.send(msg)


    client.run(TOKEN)
