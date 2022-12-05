import random
import threading

from datatype import enums


# import time


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
        self.db = {
            "SOFT8023": {
                "learning_outcomes": [
                    "Evaluate and apply design patterns in the design and development of a distributed system.",
                    "Assess and apply different architectural patterns in a distributed system",
                    "Critically access and apply threading in a distributed application.",
                    "Debug a distributed client/server application, identifying object properties and variables at "
                    "run-time.",
                    "Create a distributed object application using RMI, allowing client/server to communicate "
                    "securely via interfaces and objects."
                ],
                "assessments": [
                    "Project (An example assessment would be to create a simple client server application using "
                    "sockets) 20.0% Week 6",
                    "Project (Programming assignment(s) using the technologies covered in the lectures. Example "
                    "assignment(s) will access if a student can apply design patterns to write distributed code, "
                    "use technologies such as RMI and secure communication and information in transit.) 30.0% Week "
                    "12"],
                "courses": ["CR_KSDEV_8", "CR_KDNET_8", "CR_KCOMP_7"]
            },
            "SOFT8009": {
                "learning_outcomes": ["lo1", "lo2", "lo3"],
                "assessments": ["prog1", "prog2"],
                "courses": ["assess1", "assess2"]
            }
        }
        self.lock = threading.Lock()
        self.rand = random.random()

    def get_module_id(self, module_id):
        # self.lock.acquire()
        # time.sleep(4)
        return self.db.get(module_id)

    def get_listname(self, module_id, listname):
        # self.lock.acquire()
        # time.sleep(4)
        return self.db.get(module_id).get(listname)

    def get_listname_element(self, module_id, listname, index):
        # self.lock.acquire()
        # time.sleep(4)
        return self.db.get(module_id).get(listname)[index]

    def add_lo_element(self, module_id, info):
        # self.lock.acquire()
        # time.sleep(4)
        added_lo_element = self.db.get(module_id).get("learning_outcomes").append(info)
        result = f"{enums.OTHER_QUESTIONS.UPDATE_LO_LIST.value}\n" + self.to_string_list(module_id=module_id,
                                                                                         listname="learning_outcomes")
        # self.lock.release()
        return result

    def delete_lo_element(self, module_id, index):
        self.lock.acquire()
        # time.sleep(4)
        self.db.get(module_id).get("learning_outcomes").pop(index)
        result = f"{enums.OTHER_QUESTIONS.UPDATE_LO_LIST.value}\n" + self.to_string_list(module_id=module_id,
                                                                                         listname="learning_outcomes")
        # self.lock.release()
        return result

    def edit_lo_element(self, module_id, listname, index, new_info):
        self.lock.acquire()
        # time.sleep(4)
        self.db.get(module_id).get(listname)[index] = new_info
        result = f"{enums.OTHER_QUESTIONS.UPDATE_LO_LIST.value}\n" + self.to_string_list(module_id=module_id,
                                                                                         listname="learning_outcomes")
        # self.lock.release()
        return result

    def id_exists(self, **kwargs):
        if kwargs['module_id'] not in self.db:
            return "ID " + enums.OTHER_QUESTIONS.NOT_FOUND
        else:
            return True

    def listname_exists(self, **kwargs):
        if kwargs['list_name'] not in self.db.get(kwargs['module_id']).items():
            return "listname ".join(enums.OTHER_QUESTIONS.NOT_FOUND.value)
        else:
            return True

    def list_item_exists(self, **kwargs):
        try:
            var = self.db.get(kwargs['module_id']).get(kwargs['list_name'])[kwargs['list_item']]
            return True
        except IndexError:
            return "list-item ".join(enums.OTHER_QUESTIONS.NOT_FOUND.value)

    def to_string_list(self, **kwargs):
        list = self.get_listname(module_id=kwargs['module_id'], listname=kwargs['listname'])
        list_string = ""
        for count, ele in enumerate(list, 1):
            list_string += f"{count}. {ele}\n"
        return list_string
