# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:29:51 2019

@author: theoldestnoob
"""

import re
from random import randint
from itertools import product
from collections import Counter


class DieSet:
    def __init__(self, die_string):
        if not re.search(r"^-*\d+d\d+$", die_string):
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
        self._roll_counts = None

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
    def rollrange(self):
        return self.maxroll - self.minroll + 1

    @property
    def distribution(self):
        if self.prob_list is None:
            self.prob_list = self._distribution()
        return self.prob_list

    @property
    def roll_counts(self):
        if self._roll_counts is None:
            if self.negative:
                allrolls = product(range(self.sides * -1, 0), repeat=self.num)
            else:
                allrolls = product(range(1, self.sides + 1), repeat=self.num)
            allrolls_dict = Counter()
            for roll in allrolls:
                allrolls_dict[sum(roll)] += 1
            self._roll_counts = allrolls_dict
        return self._roll_counts

    def probability(self, num):
        if not self.minroll <= num <= self.maxroll:
            return 0
        else:
            for roll, prob in self.distribution:
                if roll == num:
                    return prob
            return 0

    def _distribution(self):
        results = []
        denominator = self.sides ** self.num
        for result in range(self.minroll, self.maxroll + 1):
            results.append((result,
                            round(self.roll_counts[result] / denominator, 5)))
        return results


class DieExpr:
    def __init__(self, dice_string):
        self.dstring = re.sub(r"\s", "", dice_string)
        self.diesets = dstring_parse(dice_string)
        self.prob_list = None
        self._roll_counts = None

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
    def rollrange(self):
        return self.maxroll - self.minroll + 1

    @property
    def distribution(self):
        if self.prob_list is None:
            self.prob_list = self._distribution()
        return self.prob_list

    @property
    def roll_counts(self):
        if self._roll_counts is None:
            # get all of our sets' roll_counts dicts in a list
            # as (key, value) tuples instead of {key: value} maps
            set_roll_tuples = []
            for dieset in self.diesets:
                set_roll_list = []
                for key, value in dieset.roll_counts.items():
                    set_roll_list.append((key, value))
                set_roll_tuples.append(set_roll_list)
            # get the product of our lists of tuples
            product_list = product(*set_roll_tuples)
            # get our roll_counts count:
            # the sum of keys is the combined roll value
            # the product (multiplication) of values is the total combinations
            roll_count = Counter()
            for roll_list in product_list:
                totalsum = 0
                totalprod = 1
                for roll, count in roll_list:
                    totalsum += roll
                    totalprod *= count
                roll_count[totalsum] += totalprod
            self._roll_counts = roll_count
        return self._roll_counts

    def probability(self, num):
        if not self.minroll <= num <= self.maxroll:
            return 0
        else:
            for roll, prob in self.distribution:
                if roll == num:
                    return prob
            return 0

    def _distribution(self):
        results = []
        denominator = 0
        for roll, count in self.roll_counts.items():
            denominator += count
        for result in range(self.minroll, self.maxroll + 1):
            results.append((result,
                            round(self.roll_counts[result] / denominator, 5)))
        return results


def dstring_tokenize(dice_string):
    # check for invalid string
    invalid_token = re.search(r"[^-+d\d\s]", dice_string)
    if invalid_token is not None:
        err = f"Invalid character '{invalid_token.group()}' in '{dice_string}'"
        raise ValueError(err)
    # strip whitespace
    dice_string = re.sub(r"\s", "", dice_string)
    # split into tokens
    d_tokens = re.split("([+-])", dice_string)
    for token in d_tokens:
        if token == "":
            err = f"Invalid token in {dice_string}, check operators"
            raise ValueError(err)
        else:
            valid_token = re.search(r"^(\d+d\d+|[+-]|\d+)$", token)
            if valid_token is None:
                raise ValueError(f"Invalid token '{token}' in {dice_string}")
    return d_tokens


def dstring_parse(dice_string):
    d_list = []
    d_tokens = dstring_tokenize(dice_string)
    negative = False
    for token in d_tokens:
        if token == "-":
            negative = True
        if re.search(r"^\d+$", token):
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
