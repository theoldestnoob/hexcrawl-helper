# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:29:51 2019

@author: theoldestnoob
"""

import re
from random import randint
from itertools import product, chain


class DieSet:
    def __init__(self, die_string):
        if not re.search("^-*\d+d\d+$", die_string):
            raise ValueError(f"Invalid die string {die_string}")
        self.dstring = die_string
        num_str, sides_str = die_string.split("d")
        num = int(num_str)
        sides = int(sides_str)
        if num < 0:
            self.negative = True
            num *= -1
        else:
            self.negative = False
        self.num = int(num)
        self.sides = int(sides)
        self.prob_list = None

    def __repr__(self):
        return f"DieSet('{self.dstring}')"

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
        if self.negative:
            total *= -1
        return total

    @property
    def maxroll(self):
        if self.negative:
            return self.num * -1
        else:
            return self.num * self.sides

    @property
    def minroll(self):
        if self.negative:
            return self.num * self.sides * -1
        else:
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
        if self.negative:
            allrolls = product(range(self.sides * -1, 0), repeat=self.num)
        else:
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
        self.diesets = dstring_parse(dice_string)
        self.prob_list = None

    def __repr__(self):
        return f"DieExpr('{self.dstring}')"

    def roll(self):
        total = 0
        for dieset in self.diesets:
            total += dieset.roll()
        return total

    @property
    def minroll(self):
        total = 0
        for dieset in self.diesets:
            total += dieset.minroll
        return total

    @property
    def maxroll(self):
        total = 0
        for dieset in self.diesets:
            total += dieset.maxroll
        return total

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

    # TODO: fix this it ain't work so good
    '''
    possibly helpful? behavior of itertools.product()
    a = [1, 2, 3]
    b = [3, 4, 5]
    c = [a, b]

    for i in product(c):
        print(i)

    ([1, 2, 3],)
    ([3, 4, 5],)

    for i in product(*c):
        print(i)

    (1, 3)
    (1, 4)
    (1, 5)
    (2, 3)
    (2, 4)
    (2, 5)
    (3, 3)
    (3, 4)
    (3, 5)
    '''
    def _probabilities(self):
        results = []
        setrolls = []
        allrolls = []
        denominator = 0
        for dieset in self.diesets:
            denominator += dieset.sides ** dieset.num
        numerator_dict = {}
        for i in range(self.minroll, self.maxroll + 1):
            numerator_dict[i] = 0
        for dieset in self.diesets:
            if dieset.negative:
                setroll = product(range(dieset.sides * -1, 0), repeat=dieset.num)
            else:
                setroll = product(range(1, dieset.sides + 1), repeat=dieset.num)
            setrolls.append(setroll)
            print(f"setroll: {setroll}")
            for roll in setroll:
                print(f"{roll}")
        print(f"setrolls: {setrolls}")
        allrolls = product(*setrolls)
        print(f"allrolls: {allrolls}")
        for roll in allrolls:
            print(f"roll: {roll}")
            numerator_dict[sum(roll)] += 1
        for result in range(self.minroll, self.maxroll + 1):
            results.append((result,
                            round(numerator_dict[result] / denominator, 5)))
        return results


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
    negative = False
    for token in d_tokens:
        if token == "-":
            negative = True
        if re.search("^\d+$", token):
            if negative:
                token = f"-{token}"
                negative = False
            d_list.append(DieSet(f"{token}d1"))
        elif token != "+" and token != "-":
            if negative:
                token = f"-{token}"
                negative = False
            d_list.append(DieSet(token))
    return d_list


def roll(dice_string):
    d_tokens = dstring_parse(dice_string)
    total = 0
    for token in d_tokens:
        total += token.roll()
    return total
