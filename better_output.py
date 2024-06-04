from __future__ import annotations
from collections.abc import Callable
from typing import Union, get_args
import sys

SUPPORTED_TYPES = Union[str, dict, list, int]
CONVERTABLE_TYPES = Union[str, int]


class Printer:
    args = get_args(SUPPORTED_TYPES)
    end: str = '\n'

    @staticmethod
    def __printf(text: str = ''):
        sys.stdout.buffer.write(text.encode('utf-8'))

    def __str_show(self, data: str, *args) -> None:
        self.__printf("'" + data + "'")

    def __int_show(self, data: int, *args) -> None:
        self.__printf(f'{data}')

    def __list_show(self, data: list, tabs: int) -> None:
        self.__printf('[')
        for i in range(len(data)):
            self.__printf('\n' + '\t' * (tabs + 1))
            self.__show(data[i], tabs + 1)
            self.__printf((self.__split[(i + 1) // len(data)]) + ('\t' * (tabs *  (i + 1) // len(data))))
        self.__printf(']')

    def __dict_show(self, data: dict, tabs: int) -> None:
        self.__printf('{')
        keys = list(data.keys())
        for i in range(len(keys)):
            self.__printf('\n' + '\t' * (tabs + 1))
            self.__show(keys[i], tabs + 1)
            self.__printf(': ')
            self.__show(data[keys[i]], tabs + 1)
            self.__printf((self.__split[(i + 1) // len(data)]) + ('\t' * tabs))
        self.__printf('}')

    def __show(self, data: SUPPORTED_TYPES, tabs: int):
        if type(data) not in list(self.funcs.keys()):
            self.error(type(data))

        self.funcs[type(data)](data, tabs)

    def show(self, data: SUPPORTED_TYPES):
        self.__show(data, 0)
        self.__printf('\n')

    def error(self, t: type):
        raise NotImplementedError(f"{t} type not implemented yet")

    @property
    def __split(self) -> tuple[str, str]:
        return self.sep, self.end

    def __init__(self, sep: str = ',', end: str = '\n'):
        self.funcs: dict[type, Callable[[SUPPORTED_TYPES, int], None]] = {
            self.args[i]: self.__getattribute__(f"_{type(self).__name__}__{self.args[i].__name__}_show")
            if f"_{type(self).__name__}__{self.args[i].__name__}_show" in dir(self)
            else self.error(type(Callable[[SUPPORTED_TYPES, int], None]))
            for i in range(len(self.args))
        }

        self.sep = sep
        self.end = end


def show(data: SUPPORTED_TYPES):
    Printer().show(data)


if __name__ == '__main__':
    p = Printer()

