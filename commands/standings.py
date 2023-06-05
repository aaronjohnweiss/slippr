from multiprocessing import Pool

from server import Server
from slippi_profile_parser import get_user_from_tag


async def standings(message):
    server_data = Server(message.guild.name)
    response = await message.channel.send('Fetching stats...')

    if(len(server_data.users) < 1):
        await response.edit(content='You must add users before performing this operation.')
        return

    previous_users = server_data.users.copy()

    pool = None

    pool_map = [v.tag for (k, v) in server_data.users.items()]

    with Pool(len(server_data.users)) as p:
        pool = p.map(get_user_from_tag, pool_map)

    for item in pool:
        server_data.users[item.uri_name] = item

    def select_elo(tuple):
        return float(tuple[1].elo)

    results = sorted(server_data.users.items(), key=select_elo, reverse=True)

    def elo_difference(current, previous):
        difference = current - previous
        if abs(difference) <= 0.1:
            return ''
        if difference > 0:
            return ' (+{0:.1f})'.format(difference)
        else:
            return ' ({0:.1f})'.format(difference)

    standings = 'Current standings: \n'
    for idx, tuple in enumerate(results):
        standings += '> ' + str(idx+1) + '. ' + str(tuple[1].name) + ' - ' + str(tuple[1].rank) + ' | ' + str("{:.1f}".format(tuple[1].elo)) + elo_difference(server_data.users[tuple[0]].elo, previous_users[tuple[0]].elo) + '\n'

    server_data.save()

    await response.edit(content=standings)