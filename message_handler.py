from commands.add import add
from commands.commands import commands
from commands.delete import delete
from commands.standings import standings


async def handle_message(client, message):
    if message.author == client.user:
        return

    if str(message.channel) != 'meleechat':
        return

    if(message.guild == None):
        print('Message did not belong to a guild. Returning.')
        return

    if message.content.startswith("!add"):
        await add(message)

    if message.content.startswith("!delete"):
        await delete(message)

    if message.content == '!standings':
        await standings(message)

    if message.content == '!commands' or message.content == '!help':
        await commands(message)

    return
