import time
from datetime import timedelta

startTime = time.time()

def get_uptime():
    delta = str(str(timedelta(seconds=(time.time() - startTime))).split('.')[0]).split(':')
    return str(delta[0] + 'h ' + delta[1] + 'm ' + delta[2] + 's')


async def uptime(message):
    msg = 'Bot uptime: ' + get_uptime()
    await message.channel.send(msg)
    return
