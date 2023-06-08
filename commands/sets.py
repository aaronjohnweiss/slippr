from multiprocessing import Pool

from server import Server
from slippi_profile_parser import get_user_from_tag

import copy


async def sets(message):
    server_data = Server(message.guild.name)
    response = await message.channel.send('Fetching set data...')

    if (len(server_data.users) < 1):
        await response.edit(content='You must add users before performing this operation.')
        return

    previous_users = copy.deepcopy(server_data.users)

    pool = None

    pool_map = [v.tag for (k, v) in server_data.users.items()]

    with Pool(len(server_data.users)) as p:
        pool = p.map(get_user_from_tag, pool_map)

    for item in pool:
        server_data.users[item.uri_name].wins = item.wins
        server_data.users[item.uri_name].losses = item.losses
        server_data.users[item.uri_name].sets = item.sets

    def set_difference(current, previous):
        difference = current - previous
        if difference == 0:
            return ''
        else:
            return ' (+{0})'.format(difference)

    def select_sets(tuple):
        return int(tuple[1].sets)

    results = sorted(server_data.users.items(), key=select_sets, reverse=True)

    standings = 'Sets played: \n'
    for idx, tuple in enumerate(results):
        standings += '> ' + str(idx+1) + '. ' + str(tuple[1].name) + ' - ' + str(tuple[1].wins) + ' / ' + str(tuple[1].losses) + '  |  ' + str(tuple[1].sets) + set_difference(server_data.users[tuple[0]].sets, previous_users[tuple[0]].sets) + '\n'

    server_data.save()

    await response.edit(content=standings)