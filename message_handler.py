from commands.add import add
from commands.commands import commands
from commands.delete import delete
from commands.sets import sets
from commands.standings import standings
from commands.users import users
from commands.uptime import uptime

async def handle_message(client, message):
    if message.author == client.user:
        return

    if str(message.channel) != 'meleechat':
        return

    if message.guild == None:
        print('Message did not belong to a guild. Returning.')
        return

    if message.content.startswith("!add"):
        await add(message)

    if message.content.startswith("!delete"):
        await delete(message)

    if message.content == '!standings':
        await standings(message)

    if message.content == '!sets':
        await sets(message)

    if message.content == '!users':
        await users(message)

    if message.content == '!commands' or message.content == '!help':
        await commands(message)

    if message.content.startswith("!uptime"):
        await uptime(message)

    return
