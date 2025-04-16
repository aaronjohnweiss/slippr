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
            if datetime.today() != self.timestamp:
                self.timestamp = datetime.today()
                self.days -= 1
                if self.is_finished():
                    self.active = False
                return True

        return False

