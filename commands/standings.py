from server import Server
from slippi_profile_parser import get_user_from_tag


async def standings(message):
    server_data = Server(message.guild.name)
    response = await message.channel.send('Fetching stats...')

    if(len(server_data.users) < 1):
        await response.edit(content='You must add users before performing this operation')
        return

    for key, value in server_data.users.items():
        server_data.users[key] = get_user_from_tag(server_data.users[key].tag)

    def select_elo(tuple):
        return float(tuple[1].elo)

    results = sorted(server_data.users.items(), key=select_elo, reverse=True)

    standings = 'Current standings: \n'
    for idx, tuple in enumerate(results):
        standings += '> ' + str(idx+1) + '. ' + str(tuple[1].name) + ' - ' + str(tuple[1].rank) + ' (' + str("{:.1f}".format(tuple[1].elo)) + ')\n'

    await response.edit(content=standings)