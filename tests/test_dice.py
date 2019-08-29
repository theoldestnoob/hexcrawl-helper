# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:41:54 2019

@author: theoldestnoob
"""

import unittest

import dice


class TestDstringTokenizer(unittest.TestCase):

    def test_dstring_tokenize_xdx(self):
        self.assertEqual(dice.dstring_tokenize("1d6"), ["1d6"])

    def test_dstring_tokenize_xdx_plus_x(self):
        self.assertEqual(dice.dstring_tokenize("1d6+1"), ["1d6", "+", "1"])

    def test_dstring_tokenize_xdx_minus_x(self):
        self.assertEqual(dice.dstring_tokenize("1d6-1"), ["1d6", "-", "1"])

    def test_dstring_tokenize_xdx_plus_xdx(self):
        self.assertEqual(dice.dstring_tokenize("1d10+1d8"),
                         ["1d10", "+", "1d8"])

    def test_dstring_tokenize_xdx_minus_xdx(self):
        self.assertEqual(dice.dstring_tokenize("1d20-1d4"),
                         ["1d20", "-", "1d4"])

    def test_dstring_tokenize_xdx_plus_xdx_plus_xdx(self):
        self.assertEqual(dice.dstring_tokenize("1d4+1d6+1d8"),
                         ["1d4", "+", "1d6", "+", "1d8"])

    def test_dstring_tokenize_xdx_minus_xdx_minus_xdx(self):
        self.assertEqual(dice.dstring_tokenize("1d4-1d6-1d8"),
                         ["1d4", "-", "1d6", "-", "1d8"])

    def test_dstring_tokenize_xdx_plus_xdx_minus_xdx(self):
        self.assertEqual(dice.dstring_tokenize("1d4+1d6-1d8"),
                         ["1d4", "+", "1d6", "-", "1d8"])

    def test_dstring_tokenize_invalid_dstring(self):
        with self.assertRaisesRegex(ValueError,
                                    "Invalid character .* in .*"):
            dice.dstring_tokenize("1f20-1d4")

    def test_dstring_tokenize_invalid_token_too_many_d(self):
        with self.assertRaisesRegex(ValueError,
                                    "Invalid token '.*' in .*"):
            dice.dstring_tokenize("1dd6")

    def test_dstring_tokenize_invalid_token_too_many_minus(self):
        with self.assertRaisesRegex(ValueError,
                                    "Invalid token in .*, check operators"):
            dice.dstring_tokenize("1d10--1d4")

    def test_dstring_tokenize_invalid_token_too_many_plus(self):
        with self.assertRaisesRegex(ValueError,
                                    "Invalid token in .*, check operators"):
            dice.dstring_tokenize("1d6++1d4")

    def test_dstring_tokenize_invalid_token_too_many_operators(self):
        with self.assertRaisesRegex(ValueError,
                                    "Invalid token in .*, check operators"):
            dice.dstring_tokenize("1d6+-1d6")

    def test_dstring_tokenize_whitespace_1d6_1(self):
        self.assertEqual(dice.dstring_tokenize("1d6 + 1"), ["1d6", "+", "1"])

    def test_dstring_tokenize_whitespace_1d6_2(self):
        self.assertEqual(dice.dstring_tokenize("1d6  +2"), ["1d6", "+", "2"])


class TestDstringParser(unittest.TestCase):

    def test_dstring_parse_xdx(self):
        self.assertEqual(dice.dstring_parse("1d6"), [dice.DieSet("1d6")])

    def test_dstring_tokenize_xdx_plus_xdx(self):
        self.assertEqual(dice.dstring_parse("1d10+1d8"),
                         [dice.DieSet("1d10"), dice.DieSet("1d8")])

    def test_dstring_tokenize_xdx_minus_xdx(self):
        self.assertEqual(dice.dstring_parse("1d20-1d4"),
                         [dice.DieSet("1d20"), dice.DieSet("-1d4")])

    def test_dstring_tokenize_xdx_plus_xdx_plus_xdx(self):
        self.assertEqual(dice.dstring_parse("1d4+1d6+1d8"),
                         [dice.DieSet("1d4"), dice.DieSet("1d6"),
                          dice.DieSet("1d8")])

    def test_dstring_tokenize_xdx_minus_xdx_minus_xdx(self):
        self.assertEqual(dice.dstring_parse("1d4-1d6-1d8"),
                         [dice.DieSet("1d4"), dice.DieSet("-1d6"),
                          dice.DieSet("-1d8")])

    def test_dstring_tokenize_xdx_plus_xdx_minus_xdx(self):
        self.assertEqual(dice.dstring_parse("1d4+1d6-1d8"),
                         [dice.DieSet("1d4"), dice.DieSet("1d6"),
                          dice.DieSet("-1d8")])


class TestDiceRoll(unittest.TestCase):

    def test_roll_1d6(self):
        self.assertTrue(1 <= dice.roll("1d6") <= 6)

    def test_roll_1d10_plus_1d8(self):
        self.assertTrue(2 <= dice.roll("1d10+1d8") <= 18)

    def test_roll_1d6_plus_4(self):
        self.assertTrue(5 <= dice.roll("1d6+4") <= 10)

    def test_roll_4_minus_2(self):
        self.assertEqual(dice.roll("4-2"), 2)

    def test_roll_4_pluss_2(self):
        self.assertEqual(dice.roll("4+2"), 6)

    def test_roll_1d6_minus_4(self):
        self.assertTrue(-3 <= dice.roll("1d6-4") <= 2)


class TestDieSet(unittest.TestCase):

    def test_DieSet_invalid_1d6_p_2(self):
        with self.assertRaisesRegex(ValueError,
                                    "Invalid die string .*"):
            dice.DieSet("1d6+2")

    def test_DieSet_invalid_1d6_p_1d4(self):
        with self.assertRaisesRegex(ValueError,
                                    "Invalid die string .*"):
            dice.DieSet("1d6+1d4")

    def test_DieSet_invalid_1s8(self):
        with self.assertRaisesRegex(ValueError,
                                    "Invalid die string .*"):
            dice.DieSet("1s8")

    def test_DieSet_repr(self):
        dieset_1d6 = dice.DieSet("1d6")
        self.assertEqual(dieset_1d6.__repr__(), "DieSet('1d6')")

    def test_DieSet_eq(self):
        dieset_1d6 = dice.DieSet("1d6")
        dieset_1d6_b = dice.DieSet("1d6")
        self.assertEqual(dieset_1d6, dieset_1d6_b)

    def test_DieSet_neq(self):
        dieset_1d6 = dice.DieSet("1d6")
        dieset_2d4 = dice.DieSet("2d4")
        self.assertNotEqual(dieset_1d6, dieset_2d4)

    def test_DieSet_roll_1d6(self):
        dieset_1d6 = dice.DieSet("1d6")
        for _ in range(1000):
            self.assertTrue(1 <= dieset_1d6.roll() <= 6)

    def test_DieSet_roll_2d4(self):
        dieset_2d4 = dice.DieSet("2d4")
        for _ in range(1000):
            self.assertTrue(2 <= dieset_2d4.roll() <= 8)

    def test_DieSet_roll_6d1(self):
        dieset_6d1 = dice.DieSet("6d1")
        for _ in range(1000):
            self.assertEqual(dieset_6d1.roll(), 6)

    def test_DieSet_roll_neg1d6(self):
        dieset_neg1d6 = dice.DieSet("-1d6")
        for _ in range(1000):
            self.assertTrue(-6 <= dieset_neg1d6.roll() <= -1)

    def test_DieSet_maxroll_1d6(self):
        dieset_1d6 = dice.DieSet("1d6")
        self.assertEqual(dieset_1d6.maxroll, 6)

    def test_DieSet_maxroll_2d4(self):
        dieset_2d4 = dice.DieSet("2d4")
        self.assertEqual(dieset_2d4.maxroll, 8)

    def test_DieSet_maxroll_6d1(self):
        dieset_6d1 = dice.DieSet("6d1")
        self.assertEqual(dieset_6d1.maxroll, 6)

    def test_DieSet_maxroll_neg1d6(self):
        dieset_neg1d6 = dice.DieSet("-1d6")
        self.assertEqual(dieset_neg1d6.maxroll, -1)

    def test_DieSet_minroll_1d6(self):
        dieset_1d6 = dice.DieSet("1d6")
        self.assertEqual(dieset_1d6.minroll, 1)

    def test_DieSet_minroll_2d4(self):
        dieset_2d4 = dice.DieSet("2d4")
        self.assertEqual(dieset_2d4.minroll, 2)

    def test_DieSet_minroll_6d1(self):
        dieset_6d1 = dice.DieSet("6d1")
        self.assertEqual(dieset_6d1.minroll, 6)

    def test_DieSet_minroll_neg1d6(self):
        dieset_neg1d6 = dice.DieSet("-1d6")
        self.assertEqual(dieset_neg1d6.minroll, -6)

    def test_DieSet_rollrange_1d6(self):
        dieset_1d6 = dice.DieSet("1d6")
        self.assertEqual(dieset_1d6.rollrange, 6)

    def test_DieSet_rollrange_2d4(self):
        dieset_2d4 = dice.DieSet("2d4")
        self.assertEqual(dieset_2d4.rollrange, 7)

    def test_DieSet_rollrange_6d1(self):
        dieset_6d1 = dice.DieSet("6d1")
        self.assertEqual(dieset_6d1.rollrange, 1)

    def test_DieSet_rollrange_neg1d6(self):
        dieset_neg1d6 = dice.DieSet("-1d6")
        self.assertEqual(dieset_neg1d6.rollrange, 6)

    def test_DieSet_distribution_1d6(self):
        dieset_1d6 = dice.DieSet("1d6")
        self.assertEqual(dieset_1d6.distribution,
                         [(1, 0.16667),
                          (2, 0.16667),
                          (3, 0.16667),
                          (4, 0.16667),
                          (5, 0.16667),
                          (6, 0.16667)])

    def test_DieSet_distribution_2d4(self):
        dieset_2d4 = dice.DieSet("2d4")
        self.assertEqual(dieset_2d4.distribution,
                         [(2, 0.0625),
                          (3, 0.125),
                          (4, 0.1875),
                          (5, 0.25),
                          (6, 0.1875),
                          (7, 0.125),
                          (8, 0.0625)])

    def test_DieSet_distribution_6d1(self):
        dieset_6d1 = dice.DieSet("6d1")
        self.assertEqual(dieset_6d1.distribution, [(6, 1)])

    def test_DieSet_distribution_3d3(self):
        dieset_3d3 = dice.DieSet("3d3")
        self.assertEqual(dieset_3d3.distribution,
                         [(3, 0.03704),
                          (4, 0.11111),
                          (5, 0.22222),
                          (6, 0.25926),
                          (7, 0.22222),
                          (8, 0.11111),
                          (9, 0.03704)])

    def test_DieSet_distribution_neg1d6(self):
        dieset_neg1d6 = dice.DieSet("-1d6")
        self.assertEqual(dieset_neg1d6.distribution,
                         [(-6, 0.16667),
                          (-5, 0.16667),
                          (-4, 0.16667),
                          (-3, 0.16667),
                          (-2, 0.16667),
                          (-1, 0.16667)])

    def test_DieSet_probability_1d6_1(self):
        dieset_1d6 = dice.DieSet("1d6")
        self.assertEqual(dieset_1d6.probability(1), 0.16667)

    def test_DieSet_probability_1d6_7(self):
        dieset_1d6 = dice.DieSet("1d6")
        self.assertEqual(dieset_1d6.probability(7), 0)

    def test_DieSet_probability_2d4_2(self):
        dieset_2d4 = dice.DieSet("2d4")
        self.assertEqual(dieset_2d4.probability(2), 0.0625)

    def test_DieSet_probability_2d4_6(self):
        dieset_2d4 = dice.DieSet("2d4")
        self.assertEqual(dieset_2d4.probability(6), 0.1875)

    def test_DieSet_probability_6d1_6(self):
        dieset_6d1 = dice.DieSet("6d1")
        self.assertEqual(dieset_6d1.probability(6), 1)

    def test_DieSet_probability_6d1_5(self):
        dieset_6d1 = dice.DieSet("6d1")
        self.assertEqual(dieset_6d1.probability(5), 0)

    def test_DieSet_probability_neg1d6_3(self):
        dieset_neg1d6 = dice.DieSet("-1d6")
        self.assertEqual(dieset_neg1d6.probability(3), 0)

    def test_DieSet_probability_neg1d6_neg3(self):
        dieset_neg1d6 = dice.DieSet("-1d6")
        self.assertEqual(dieset_neg1d6.probability(-3), 0.16667)


class TestDieExpr(unittest.TestCase):

    def test_DieExpr_repr_1d6(self):
        dieexpr_1d6 = dice.DieExpr("1d6")
        self.assertEqual(dieexpr_1d6.__repr__(), "DieExpr('1d6')")

    def test_DieExpr_repr_2d4(self):
        dieexpr_2d4 = dice.DieExpr("2d4")
        self.assertEqual(dieexpr_2d4.__repr__(), "DieExpr('2d4')")

    def test_DieExpr_repr_1d6_p_1d4(self):
        dieexpr_1d6_p_1d4 = dice.DieExpr("1d6+1d4")
        self.assertEqual(dieexpr_1d6_p_1d4.__repr__(),
                         "DieExpr('1d6+1d4')")

    def test_DieExpr_repr_1d6_m_1d4(self):
        dieexpr_1d6_m_1d4 = dice.DieExpr("1d6-1d4")
        self.assertEqual(dieexpr_1d6_m_1d4.__repr__(),
                         "DieExpr('1d6-1d4')")

    def test_DieExpr_repr_1d10_m_2(self):
        dieexpr_1d10_m_2 = dice.DieExpr("1d10-2")
        self.assertEqual(dieexpr_1d10_m_2.__repr__(), "DieExpr('1d10-2')")

    def test_DieExpr_repr_1d8_1d10_1d4_m_2(self):
        dieexpr_1d8_1d10_1d4_m_2 = dice.DieExpr("1d8+1d10+1d4-2")
        self.assertEqual(dieexpr_1d8_1d10_1d4_m_2.__repr__(),
                         "DieExpr('1d8+1d10+1d4-2')")

    def test_DieExpr_repr_whitespace(self):
        dieexpr_1d6_p_1d4 = dice.DieExpr("1 d6  +   1d  4")
        self.assertEqual(dieexpr_1d6_p_1d4.__repr__(),
                         "DieExpr('1d6+1d4')")

    def test_DieExpr_roll_1d6(self):
        dieexpr_1d6 = dice.DieExpr("1d6")
        for _ in range(1000):
            self.assertTrue(1 <= dieexpr_1d6.roll() <= 6)

    def test_DieExpr_roll_2d4(self):
        dieexpr_2d4 = dice.DieExpr("2d4")
        for _ in range(1000):
            self.assertTrue(2 <= dieexpr_2d4.roll() <= 8)

    def test_DieExpr_roll_1d6_p_1d4(self):
        dieexpr_1d6_p_1d4 = dice.DieExpr("1d6+1d4")
        for _ in range(1000):
            self.assertTrue(2 <= dieexpr_1d6_p_1d4.roll() <= 10)

    def test_DieExpr_roll_1d6_m_1d4(self):
        dieexpr_1d6_m_1d4 = dice.DieExpr("1d6-1d4")
        for _ in range(1000):
            self.assertTrue(-3 <= dieexpr_1d6_m_1d4.roll() <= 5)

    def test_DieExpr_roll_1d10_m_2(self):
        dieexpr_1d10_m_2 = dice.DieExpr("1d10-2")
        for _ in range(1000):
            self.assertTrue(-1 <= dieexpr_1d10_m_2.roll() <= 8)

    def test_DieExpr_roll_1d8_1d10_1d4_m_2(self):
        dieexpr_1d8_1d10_1d4_m_2 = dice.DieExpr("1d8+1d10+1d4-2")
        for _ in range(1000):
            self.assertTrue(1 <= dieexpr_1d8_1d10_1d4_m_2.roll() <= 20)

    def test_DieExpr_minroll_1d6(self):
        dieexpr_1d6 = dice.DieExpr("1d6")
        self.assertEqual(dieexpr_1d6.minroll, 1)

    def test_DieExpr_minroll_2d4(self):
        dieexpr_2d4 = dice.DieExpr("2d4")
        self.assertEqual(dieexpr_2d4.minroll, 2)

    def test_DieExpr_minroll_1d6_p_1d4(self):
        dieexpr_1d6_p_1d4 = dice.DieExpr("1d6+1d4")
        self.assertEqual(dieexpr_1d6_p_1d4.minroll, 2)

    def test_DieExpr_minroll_1d6_m_1d4(self):
        dieexpr_1d6_m_1d4 = dice.DieExpr("1d6-1d4")
        self.assertEqual(dieexpr_1d6_m_1d4.minroll, -3)

    def test_DieExpr_minroll_1d10_m_2(self):
        dieexpr_1d10_m_2 = dice.DieExpr("1d10-2")
        self.assertEqual(dieexpr_1d10_m_2.minroll, -1)

    def test_DieExpr_minroll_1d8_1d10_1d4_m_2(self):
        dieexpr_1d8_1d10_1d4_m_2 = dice.DieExpr("1d8+1d10+1d4-2")
        self.assertEqual(dieexpr_1d8_1d10_1d4_m_2.minroll, 1)

    def test_DieExpr_maxroll_1d6(self):
        dieexpr_1d6 = dice.DieExpr("1d6")
        self.assertEqual(dieexpr_1d6.maxroll, 6)

    def test_DieExpr_maxroll_2d4(self):
        dieexpr_2d4 = dice.DieExpr("2d4")
        self.assertEqual(dieexpr_2d4.maxroll, 8)

    def test_DieExpr_maxroll_1d6_p_1d4(self):
        dieexpr_1d6_p_1d4 = dice.DieExpr("1d6+1d4")
        self.assertEqual(dieexpr_1d6_p_1d4.maxroll, 10)

    def test_DieExpr_maxroll_1d6_m_1d4(self):
        dieexpr_1d6_m_1d4 = dice.DieExpr("1d6-1d4")
        self.assertEqual(dieexpr_1d6_m_1d4.maxroll, 5)

    def test_DieExpr_maxroll_1d10_m_2(self):
        dieexpr_1d10_m_2 = dice.DieExpr("1d10-2")
        self.assertEqual(dieexpr_1d10_m_2.maxroll, 8)

    def test_DieExpr_maxroll_1d8_1d10_1d4_m_2(self):
        dieexpr_1d8_1d10_1d4_m_2 = dice.DieExpr("1d8+1d10+1d4-2")
        self.assertEqual(dieexpr_1d8_1d10_1d4_m_2.maxroll, 20)

    def test_DieSet_rollrange_1d6(self):
        dieexpr_1d6 = dice.DieExpr("1d6")
        self.assertEqual(dieexpr_1d6.rollrange, 6)

    def test_DieSet_rollrange_2d4(self):
        dieexpr_2d4 = dice.DieExpr("2d4")
        self.assertEqual(dieexpr_2d4.rollrange, 7)

    def test_DieSet_rollrange_1d6_p_1d4(self):
        dieexpr_1d6_p_1d4 = dice.DieExpr("1d6+1d4")
        self.assertEqual(dieexpr_1d6_p_1d4.rollrange, 9)

    def test_DieSet_rollrange_1d6_m_1d4(self):
        dieexpr_1d6_m_1d4 = dice.DieExpr("1d6-1d4")
        self.assertEqual(dieexpr_1d6_m_1d4.rollrange, 9)

    def test_DieSet_rollrange_1d10_m_2(self):
        dieexpr_1d10_m_2 = dice.DieExpr("1d10-2")
        self.assertEqual(dieexpr_1d10_m_2.rollrange, 10)

    def test_DieSet_rollrange_1d8_1d10_1d4_m_2(self):
        dieexpr_1d8_1d10_1d4_m_2 = dice.DieExpr("1d8+1d10+1d4-2")
        self.assertEqual(dieexpr_1d8_1d10_1d4_m_2.rollrange, 20)

    def test_DieExpr_distribution_1d6(self):
        dieexpr_1d6 = dice.DieExpr("1d6")
        self.assertEqual(dieexpr_1d6.distribution,
                         [(1, 0.16667),
                          (2, 0.16667),
                          (3, 0.16667),
                          (4, 0.16667),
                          (5, 0.16667),
                          (6, 0.16667)])

    def test_DieExpr_distribution_2d4(self):
        dieexpr_2d4 = dice.DieExpr("2d4")
        self.assertEqual(dieexpr_2d4.distribution,
                         [(2, 0.0625),
                          (3, 0.125),
                          (4, 0.1875),
                          (5, 0.25),
                          (6, 0.1875),
                          (7, 0.125),
                          (8, 0.0625)])

    def test_DieExpr_distribution_1d6_p_1d4(self):
        dieexpr_1d6_p_1d4 = dice.DieExpr("1d6+1d4")
        self.assertEqual(dieexpr_1d6_p_1d4.distribution,
                         [(2, 0.04167),
                          (3, 0.08333),
                          (4, 0.125),
                          (5, 0.16667),
                          (6, 0.16667),
                          (7, 0.16667),
                          (8, 0.125),
                          (9, 0.08333),
                          (10, 0.04167)])

    def test_DieExpr_distribution_1d6_m_1d4(self):
        dieexpr_1d6_m_1d4 = dice.DieExpr("1d6-1d4")
        self.assertEqual(dieexpr_1d6_m_1d4.distribution,
                         [(-3, 0.04167),
                          (-2, 0.08333),
                          (-1, 0.125),
                          (0, 0.16667),
                          (1, 0.16667),
                          (2, 0.16667),
                          (3, 0.125),
                          (4, 0.08333),
                          (5, 0.04167)])

    def test_DieExpr_distribution_1d10_m_2(self):
        dieexpr_1d10_m_2 = dice.DieExpr("1d10-2")
        self.assertEqual(dieexpr_1d10_m_2.distribution,
                         [(-1, 0.1),
                          (0, 0.1),
                          (1, 0.1),
                          (2, 0.1),
                          (3, 0.1),
                          (4, 0.1),
                          (5, 0.1),
                          (6, 0.1),
                          (7, 0.1),
                          (8, 0.1)])

    def test_DieExpr_distribution_1d8_1d10_1d4_m_2(self):
        dieexpr_1d8_1d10_1d4_m_2 = dice.DieExpr("1d8+1d10+1d4-2")
        self.assertEqual(dieexpr_1d8_1d10_1d4_m_2.distribution,
                         [(1, 0.00313),
                          (2, 0.00937),
                          (3, 0.01875),
                          (4, 0.03125),
                          (5, 0.04375),
                          (6, 0.05625),
                          (7, 0.06875),
                          (8, 0.08125),
                          (9, 0.09062),
                          (10, 0.09688),
                          (11, 0.09688),
                          (12, 0.09062),
                          (13, 0.08125),
                          (14, 0.06875),
                          (15, 0.05625),
                          (16, 0.04375),
                          (17, 0.03125),
                          (18, 0.01875),
                          (19, 0.00937),
                          (20, 0.00313)])

    def test_DieExpr_probability_1d6_1(self):
        dieexpr_1d6 = dice.DieExpr("1d6")
        self.assertEqual(dieexpr_1d6.probability(1), 0.16667)

    def test_DieExpr_probability_1d6_7(self):
        dieexpr_1d6 = dice.DieExpr("1d6")
        self.assertEqual(dieexpr_1d6.probability(7), 0)

    def test_DieExpr_probability_2d4_2(self):
        dieexpr_2d4 = dice.DieExpr("2d4")
        self.assertEqual(dieexpr_2d4.probability(2), 0.0625)

    def test_DieExpr_probability_2d4_6(self):
        dieexpr_2d4 = dice.DieExpr("2d4")
        self.assertEqual(dieexpr_2d4.probability(6), 0.1875)

    def test_DieExpr_probability_1d6_p_1d4_4(self):
        dieexpr_1d6_p_1d4 = dice.DieExpr("1d6+1d4")
        self.assertEqual(dieexpr_1d6_p_1d4.probability(4), 0.125)

    def test_DieExpr_probability_1d6_m_1d4_neg4(self):
        dieexpr_1d6_m_1d4 = dice.DieExpr("1d6-1d4")
        self.assertEqual(dieexpr_1d6_m_1d4.probability(-4), 0)

    def test_DieExpr_probability_1d10_m_2_0(self):
        dieexpr_1d10_m_2 = dice.DieExpr("1d10-2")
        self.assertEqual(dieexpr_1d10_m_2.probability(0), 0.1)

    def test_DieExpr_probability_1d8_1d10_1d4_m_2_9(self):
        dieexpr_1d8_1d10_1d4_m_2 = dice.DieExpr("1d8+1d10+1d4-2")
        self.assertEqual(dieexpr_1d8_1d10_1d4_m_2.probability(9), 0.09062)


if __name__ == "__main__":
    unittest.main()
