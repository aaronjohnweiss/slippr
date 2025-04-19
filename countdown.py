from datetime import datetime
class Countdown:

    def __init__(self, days, reason):
        self.timestamp = datetime.today()
        try:
            self.days = int(days)
        except ValueError as e:
            raise e
        self.reason = reason
        self.active = False
        if not self.is_finished():
            self.active = True

    def is_finished(self):
        if self.days > 0:
            return False
        else:
            return True

    def decrement(self):
        if self.active:
            if abs(datetime.today() - self.timestamp).days > 0:
                self.timestamp = datetime.today()
                self.days -= 1
                if self.is_finished():
                    self.active = False
                return True

        return False

    def status(self):
        msg = ''
        if self.active:
            if self.days == 1:
                msg = 'There is ' + str(self.days) + ' day remaining until ' + str(
                    self.reason) + '.'
            else:
                msg = 'There are ' + str(self.days) + ' days remaining until ' + str(
                    self.reason) + '.'
        else:
            msg = 'Countdown for ' + str(self.reason) + ' finished!'
        return msg
