from tinydb import TinyDB, Query

import random
import threading
import time


class StudentModulesDao:
    __instance = None

    @staticmethod
    def get_instance():
        if StudentModulesDao.__instance is None:
            with threading.Lock():
                if StudentModulesDao.__instance is None:  # Double locking mechanism
                    StudentModulesDao()
        return StudentModulesDao.__instance

    def __init__(self):
        if StudentModulesDao.__instance is not None:
            raise Exception("This is a singleton!")
        else:
            StudentModulesDao.__instance = self
        self.db = TinyDB('db.json')
        self.lock = threading.Lock()
        self.rand = random.random()

    def add(self, match):
        self.lock.acquire()

        time.sleep(4)

        Module = Query()
        if not self.db.contains(Module.player1 == match.player1):
            self.db.insert({'type': match.type, 'player1': match.player1, 'player2': match.player2})

        print('Insert attempted on ' + match.player1 + '    ' + str(self.rand))

        self.lock.release()
