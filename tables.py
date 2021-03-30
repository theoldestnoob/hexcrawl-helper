# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:17:43 2019

@author: theoldestnoob
"""
from __future__ import annotations
from random import randint

import dice


class TableEntry:
    def __init__(self, name: str, priority: int = 99, pos_wt: int = 0,
                 prob_wt: int = 0, notes: str = None) -> None:
        # brief description of table entry
        self.name = name
        # priority of entry: lower = higher priority
        self.priority = priority
        # position weight
        #   positive if entry wants to be high on table
        #   negative if entry wants to be low on table
        #   magnitude determines how much it wants to be high or low
        self.pos_weight = pos_wt
        # probability weight
        #   positive if entry wants to be more probable
        #   negative if entry wants to be less probable
        self.prob_weight = prob_wt
        # longer string for more detail on entry
        self.notes = notes

    def __eq__(self, other) -> bool:
        return (self.name == other.name
                and self.priority == other.priority
                and self.pos_weight == other.pos_weight
                and self.prob_weight == other.prob_weight
                and self.notes == other.notes)

    def get_entry(self, depth: int = 0) -> TableEntry:
        return self


class Table:
    def __init__(self, name: str, diestr: dice.DieSet = None,
                 entries: list[TableEntry] = None) -> None:
        self.name = name
        if entries is not None:
            self._entries = entries
        else:
            self._entries = []
        self._table = []
        self.set_dice(diestr)
        self.gen_table()

    def append(self, entry) -> None:
        self._entries.append(entry)
        self._changed = True

    def remove(self, entry) -> None:
        self._entries.remove(entry)
        self._changed = True

    def clear(self, entry) -> None:
        self._entries.clear()
        self._changed = True

    def __str__(self) -> str:
        return self.name

    def __len__(self) -> int:
        if self._dice is None:
            return len(self._entries)
        else:
            return self._dice.rollrange

    # TODO: rewrite __getitem__ and get_entry to accomodate large tables
    #       with passed-in modifiers that exceed the dice
    #       and/or custom dice passed to get the item
    def __getitem__(self, position: int) -> TableEntry:
        if self._changed:
            self.gen_table()
        index = 1
        if self._dice is not None:
            if position < self._dice.minroll or position > self._dice.maxroll:
                raise IndexError
            index = self._dice.minroll
        return self._table[position - index]

    def get_entry(self, depth: int = 0) -> TableEntry:
        if depth > 10:
            error_entry = TableEntry('Error: Recursive Tables')
            return error_entry
        if self._dice is None:
            index = randint(1, len(self._entries))
        else:
            index = self._dice.roll()
        if hasattr(self.__getitem__(index), 'get_entry'):
            return self.__getitem__(index).get_entry(depth + 1)
        else:
            return self.__getitem__(index)

    def set_dice(self, diestr) -> None:
        if diestr is None:
            self._dice = None
        else:
            self._dice = dice.DieSet(diestr)
        self._changed = True

    # TODO: it seems silly to have a get_name function instead of just
    #       directly accessing the attribute on the other hand, there may be
    #       value as part of a function for *display* access vs *roll* access
    def get_name(self) -> str:
        return self.name

    def gen_table(self) -> None:
        if self._dice is None:
            for e in self._entries:
                self._table.append(e)
        else:
            tablesize = self._dice.rollrange
            table = sorted(self._entries, key=lambda entry: entry.prob_weight,
                           reverse=True)
            table = sorted(self._entries, key=lambda entry: entry.priority)
            self._table = table[:tablesize]
        self._changed = False
