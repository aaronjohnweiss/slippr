from server import Server
from user import User


async def delete(message):
    server_data = Server(message.guild.name)
    print(str(server_data.users))
    response = await message.channel.send('Deleting user...')
    tag = message.content.split()[1]

    msg = ''
    try:
        temp_user = User(tag)
        msg = 'User ' + tag + ' removed from the channel standings.'

        del server_data.users[temp_user.uri_name]
        server_data.save()
    except KeyError:
        msg = 'Could not remove user: ' + tag + ' does not exist.'
    await response.edit(content=msg)