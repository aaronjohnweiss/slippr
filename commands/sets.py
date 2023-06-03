from multiprocessing import Pool

from server import Server
from slippi_profile_parser import get_user_from_tag


async def sets(message):
    server_data = Server(message.guild.name)
    response = await message.channel.send('Fetching set data...')

    if (len(server_data.users) < 1):
        await response.edit(content='You must add users before performing this operation')
        return

    # pool = None
    #
    # print('Creating thread pool..')
    # with Pool(len(server_data.users)) as p:
    #     pool = p.map(get_user_from_tag, server_data.users.keys())
    #
    # print('Cleaning up thread results..')
    # for item in pool:
    #     server_data.users[item.uri_name] = item

    for key, value in server_data.users.items():
        server_data.users[key] = get_user_from_tag(server_data.users[key].tag)

    def select_sets(tuple):
        return int(tuple[1].sets)

    results = sorted(server_data.users.items(), key=select_sets, reverse=True)

    standings = 'Sets played: \n'
    for idx, tuple in enumerate(results):
        standings += '> ' + str(idx+1) + '. ' + str(tuple[1].name) + ' - ' + str(tuple[1].wins) + ' / ' + str(tuple[1].losses) + ' (' + str(tuple[1].sets) + ')\n'

    await response.edit(content=standings)