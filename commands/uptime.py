import time
from datetime import timedelta
from threading import Timer
from uptime_history import UptimeHistory

startTime = time.time()

uptime_history = UptimeHistory()
uptime_history.add_session()


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


timer = RepeatTimer(30, uptime_history.update_current_session)
timer.start()


def get_uptime():
    delta = str(str(timedelta(seconds=(time.time() - startTime))).split('.')[0]).split(':')
    return str(delta[0] + 'h ' + delta[1] + 'm ' + delta[2] + 's')


async def uptime(message):
    msg = 'Bot uptime: ' + get_uptime() + '\n' + uptime_history.get_stats_message()
    await message.channel.send(msg)
    return
