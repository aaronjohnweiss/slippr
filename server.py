import os
import pickle

def load(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def dump(x, path):
    with open(path, 'wb') as f:
        pickle.dump(x, f, protocol=pickle.HIGHEST_PROTOCOL)

def get_path(name):
    return './servers/' + str(name) + '.pkl'
class Server:

    def __init__(self, name):
        self.users = dict()
        if os.path.isfile('servers/' + str(name) + '.pkl'):
            print('  loading from pickle file.')
            self.__dict__ = load(get_path(name))
        else:
            print('  creating from scratch.')
            self.name = name
            dump(self.__dict__, get_path(name))

        print('Server ' + self.name + ' initialized.')

    def save(self):
        print('Saving file ' + get_path(self.name))
        dump(self.__dict__, get_path(self.name))

