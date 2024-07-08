import os
import pickle
import time
from datetime import timedelta
startTime = time.time()

def load(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def dump(x, path):
    with open(path, 'wb') as f:
        pickle.dump(x, f, protocol=pickle.HIGHEST_PROTOCOL)

def metadata_path():
    return './metadata/uptime-history.pkl'



class UptimeHistory:


    def __init__(self):
        self.history = []
        if not os.path.exists('./metadata'):
            os.makedirs('./metadata')
        if os.path.isfile(metadata_path()):
            self.__dict__ = load(metadata_path())
        else:
            print('Creating metadata file ' + metadata_path())
            dump(self.__dict__, metadata_path())
        print('History length: ' + str(len(self.history)))

    def save(self):
        # print('Saving file ' + metadata_path())
        dump(self.__dict__, metadata_path())

    def add_session(self):
        new_entry = {
            'start': time.time(),
            'end': time.time()
        }

        self.history.append(new_entry)
        self.save()

    def update_current_session(self):
        if len(self.history) < 1:
            self.add_session()
            print('No sessions to update - returning')
            return
        self.history[-1]['end'] = time.time()
        self.save()

    def get_stats_message(self):
        if len(self.history) < 1:
            return 'No uptime history found.'
        if len(self.history) == 1:
            return 'No previous outages.'

        delta = str(str(timedelta(seconds=(self.history[-1]['start'] - self.history[-2]['end']))).split('.')[0]).split(':')
        outage = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.history[-2]['end']))
        duration = str(delta[0] + 'h ' + delta[1] + 'm ' + delta[2] + 's')
        return 'Previous outage: ' + outage + '\n' + 'Previous outage duration: ' + duration

