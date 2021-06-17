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
        #   positive if entry wants to be more probable (center)
        #   negative if entry wants to be less probable (edges)
        #   magnitude determines how central or edgy it wants to be
        self.prob_weight = prob_wt
        # combined weight
        #   combined position and probability weights
        #   derived value determined on table generation
        self._weight = 0
        # longer string for more detail on entry
        self.notes = notes

    def __eq__(self, other) -> bool:
        return (self.name == other.name
                and self.priority == other.priority
                and self.pos_weight == other.pos_weight
                and self.prob_weight == other.prob_weight
                and self.notes == other.notes)

    def get_entry(self, *args, **kwargs) -> TableEntry:
        return self


class Table(TableEntry):
    def __init__(self, name: str, diestr: dice.DieSet = None,
                 priority: int = 99, pos_wt: int = 0, prob_wt: int = 0,
                 entries: list[TableEntry] = None) -> None:
        self.name = name
        self.priority = priority
        self.pos_weight = pos_wt
        self.prob_weight = prob_wt
        if entries is not None:
            self._entries = entries
        else:
            self._entries = []
        self._table = []
        self.set_dice(diestr)

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
        if self._dice is not None:
            if position < self._dice.minroll or position > self._dice.maxroll:
                raise IndexError
            index = self._dice.minroll
        else:
            if position < 1 or position > len(self._entries):
                raise IndexError
            index = 1
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

    # TODO: replace the set_dice() method with set_size() method
    #       and push dice and random functionality up to a container class
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
            tablesize = len(self._entries)
        else:
            tablesize = self._dice.rollrange
        if tablesize == 0:
            self._table = []
            return
        # sort on entry priority and cut table down to size
        #  first sort on probability so we drop low probability entries first
        table = sorted(self._entries, key=lambda entry: entry.prob_weight,
                       reverse=True)
        table = sorted(table, key=lambda entry: entry.priority)
        table = table[:tablesize]
        # determine if multiple position weights
        one_pos_weight = True
        e_zero_wt = table[0].pos_weight
        for e in table:
            if e.pos_weight != e_zero_wt:
                one_pos_weight = False
        # for multiple position weights we split the table into two
        #  and derive a combined position + probability weight
        if not one_pos_weight:
            # sort on position weight
            table = sorted(table, key=lambda entry: entry.pos_weight)
            # split into top and bottom half
            halfway = len(table) // 2
            table_bottom = table[:halfway]
            table_top = table[halfway:]
            # add probability to bottom half (higher = more central)
            # subtract probability from top half (lower = more central)
            for e in table_bottom:
                e._weight = e.pos_weight + e.prob_weight
            for e in table_top:
                e._weight = e.pos_weight - e.prob_weight
            # combine halves to make a complete sorted table
            table_bottom = sorted(table_bottom, key=lambda e: e._weight)
            table_top = sorted(table_top, key=lambda e: e._weight)
            table = table_bottom
            table.extend(table_top)
        # for a single position weight we split the table by probability
        #  and distribute evenly between the halves in order
        else:
            probdict = {}
            table_bottom = []
            table_top = []
            bottom = True
            # split into lists by probability weight
            for e in table:
                if e.prob_weight not in probdict.keys():
                    probdict[e.prob_weight] = [e]
                else:
                    probdict[e.prob_weight].append(e)
            # distribute across two halves of table in order by probability
            for key in sorted(probdict.keys(), key=lambda prob: prob,
                              reverse=True):
                for e in probdict[key]:
                    if bottom:
                        table_bottom.insert(0, e)
                        bottom = False
                    else:
                        table_top.append(e)
                        bottom = True
            # combine two table halves
            table = table_bottom
            table.extend(table_top)
        self._table = table
        self._changed = False
