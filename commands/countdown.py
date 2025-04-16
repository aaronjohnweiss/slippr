from server import Server
from countdown import Countdown


async def countdown_message(message):
    server_data = Server(message.guild.name)
    response = await message.channel.send('Starting countdown...')
    msg = ''
    try:

        split = message.content.split(maxsplit=2)
        days = split[1]
        reason = split[2]

        if days is None or reason is None:
            raise ValueError
        new_countdown = Countdown(days, reason)
        msg = 'Countdown for ' + reason + ' started! Days remaining: ' + str(days) + '.'
        server_data.countdown = new_countdown
        server_data.save()
    except ValueError as e:
        print(str(e))
        msg = 'Need to provide duration (days) and reason, ex: !countdown 3 reason'
    await response.edit(content=msg)