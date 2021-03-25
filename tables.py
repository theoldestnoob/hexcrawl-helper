# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:17:43 2019

@author: theoldestnoob
"""

from random import randint

import dice


class Table:
    def __init__(self, name, diestr=None, entries=None):
        self.name = name
        self.set_dice(diestr)
        if entries is not None:
            self._entries = entries
        else:
            self._entries = []

    def append(self, entry):
        self._entries.append(entry)

    def __str__(self):
        return self.name

    def __len__(self):
        if self._dice is None:
            return len(self._entries)
        else:
            return self._dice.rollrange

    def __getitem__(self, position):
        index = 1
        if self._dice is not None:
            if position < self._dice.minroll or position > self._dice.maxroll:
                raise IndexError
            index = self._dice.minroll
        return self._entries[position - index]

    def get_name(self):
        return self.name

    def get_entry(self, depth=0):
        if depth > 10:
            return 'Error: Maximum Recursion'
        if self._dice is None:
            index = randint(1, len(self._entries))
        else:
            index = self._dice.roll()
        if hasattr(self.__getitem__(index), 'get_entry'):
            return self.__getitem__(index).get_entry(depth + 1)
        else:
            return self.__getitem__(index)

    def set_dice(self, diestr):
        if diestr is None:
            self._dice = None
        else:
            self._dice = dice.DieSet(diestr)
