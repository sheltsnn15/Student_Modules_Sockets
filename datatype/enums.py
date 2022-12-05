# from enum import StrEnum
from enum import Enum


class OTHER_QUESTIONS(str, Enum):
    ENTER_MOD_ID = "What is the module id? "
    UPDATE_LO_LIST = "Updated LO List: "
    ENTER_LO_NUM = "Enter LO #: "
    NOT_FOUND = "Item Not Found"
    INVALID_INPUT = "Invalid Input"
    NEW_LO_DESC = "Enter new LO description: "
    ENTER_NEW_TEXT = "Enter new text: "


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


def to_string(enum):
    lines = ""
    for member in enum:
        lines += f"{member.value} "
    return lines
