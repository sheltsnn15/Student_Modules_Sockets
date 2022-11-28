# from enum import StrEnum
import collections
from enum import Enum


class OTHER_QUESTIONS(str, Enum):
    mod_id = "What is the module id? "
    lo_list = "Updated LO List: \n"
    lo_num = "Enter LO #: "


class VIEWS(str, Enum):
    L = "(L)earning Outcomes"
    C = "(C)ourses"
    A = "(A)ssessments"
    X = "e(X)it?"


class CRUD(str, Enum):
    A = "(A)dd"
    E = "(E)dit"
    D = "(D)elete"
    R = "(R)eturn"


print(VIEWS.A.value)
