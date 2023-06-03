from server import Server


async def users(message):
    server_data = Server(message.guild.name)

    if (len(server_data.users) < 1):
        await message.channel.send('You must add users before performing this operation.')
        return

    def select_name(tuple):
        return tuple[1].name

    results = sorted(server_data.users.items(), key=select_name)

    msg = 'Users: \n'
    for idx, tuple in enumerate(results):
        msg += '> ' + str(tuple[1].name) + ' - ' + str(tuple[1].tag).upper() + '\n'

    await message.channel.send(msg)