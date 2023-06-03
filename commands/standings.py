from multiprocessing import Pool

from server import Server
from slippi_profile_parser import get_user_from_tag


async def standings(message):
    server_data = Server(message.guild.name)
    response = await message.channel.send('Fetching stats...')

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