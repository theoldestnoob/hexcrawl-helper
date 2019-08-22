# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:29:51 2019

@author: theoldestnoob
"""

import re
from random import randint
from itertools import product


class DieSet:
    def __init__(self, num, sides):
        self.num = int(num)
        self.sides = int(sides)
        self.prob_list = None

    def __repr__(self):
        return f"DieSet({self.num}, {self.sides})"

    def __eq__(self, other):
        if isinstance(other, DieSet):
            return (self.num == other.num and self.sides == other.sides)
        else:
            return NotImplemented

    def roll(self):
        total = 0
        if self.sides == 1:
            total = self.num
        else:
            for _ in range(self.num):
                total += randint(1, self.sides)
        return total

    @property
    def maxroll(self):
        return self.num * self.sides

    @property
    def minroll(self):
        return self.num

    @property
    def probabilities(self):
        if self.prob_list is None:
            self.prob_list = self._probabilities()
        return self.prob_list

    def probability(self, num):
        if not self.minroll <= num <= self.maxroll:
            return 0
        else:
            for roll, prob in self.probabilities:
                if roll == num:
                    return prob
            return 0

    def _probabilities(self):
        results = []
        denominator = self.sides ** self.num
        numerator_dict = {}
        for i in range(self.minroll, self.maxroll + 1):
            numerator_dict[i] = 0
        allrolls = product(range(1, self.sides + 1), repeat=self.num)
        for roll in allrolls:
            numerator_dict[sum(roll)] += 1
        for result in range(self.minroll, self.maxroll + 1):
            results.append((result,
                            round(numerator_dict[result] / denominator, 5)))
        return results


class DieExpr:
    def __init__(self, dice_string):
        self.dstring = dice_string
        self.addlist = []
        self.sublist = []
        d_tokens = dstring_parse(dice_string)
        add = False
        sub = False
        for token in d_tokens:
            if token == "+":
                add = True
            elif token == "-":
                sub = True
            else:
                if not add and not sub:
                    self.addlist.append(token)
                elif add:
                    add = False
                    self.addlist.append(token)
                elif sub:
                    sub = False
                    self.sublist.append(token)

    def __repr__(self):
        return f"DieExpr('{self.dstring}')"

    def roll(self):
        total = 0
        for dieset in self.addlist:
            total += dieset.roll()
        for dieset in self.sublist:
            total -= dieset.roll()
        return total

    @property
    def minroll(self):
        total = 0
        for dieset in self.addlist:
            total += dieset.minroll
        for dieset in self.sublist:
            total -= dieset.maxroll
        return total

    @property
    def maxroll(self):
        total = 0
        for dieset in self.addlist:
            total += dieset.maxroll
        for dieset in self.sublist:
            total -= dieset.minroll
        return total

    def _probabilities(self):
        pass


def dstring_tokenize(dice_string):
    # check for invalid string
    invalid_token = re.search("[^-+d\d]", dice_string)
    if invalid_token is not None:
        raise ValueError(f"Invalid character '{invalid_token.group()}' in '{dice_string}'")
    d_tokens = re.split("([+-])", dice_string)
    for token in d_tokens:
        if token == "":
            raise ValueError(f"Invalid token in {dice_string}, check operators")
        else:
            valid_token = re.search("^(\d+d\d+|[+-]|\d+)$", token)
            if valid_token is None:
                raise ValueError(f"Invalid token {token} in {dice_string}")
    return d_tokens


def dstring_parse(dice_string):
    d_list = []
    d_tokens = dstring_tokenize(dice_string)
    for token in d_tokens:
        if re.search("^\d+$", token):
            d_list.append(DieSet(token, 1))
        elif token != "+" and token != "-":
            num, sides = token.split("d")
            d_list.append(DieSet(num, sides))
        else:
            d_list.append(token)
    return d_list


def roll(dice_string):
    d_tokens = dstring_parse(dice_string)
    total = 0
    add = False
    sub = False
    for token in d_tokens:
        if token == "+":
            add = True
        elif token == "-":
            sub = True
        else:
            if not add and not sub:
                total += token.roll()
            elif add:
                add = False
                total += token.roll()
            elif sub:
                sub = False
                total -= token.roll()
    return total
