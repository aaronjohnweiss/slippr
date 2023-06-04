from server import Server
from slippi_profile_parser import get_user_from_tag


async def add(message):
    server_data = Server(message.guild.name)
    response = await message.channel.send('Adding user...')
    msg = ''
    try:
        tag = message.content.split()[1]
        user = get_user_from_tag(tag)
        msg = 'User ' + user.name + ' added to the channel standings.'

        server_data.users[user.uri_name] = user
        server_data.save()
    except:
        msg = 'Failed to add user - did you use a valid Slippi tag?'
    await response.edit(content=msg)