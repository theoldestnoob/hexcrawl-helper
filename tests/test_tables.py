# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:28:40 2019

@author: theoldestnoob
"""

import unittest

import tables


class TestTable(unittest.TestCase):

    def setUp(self):
        self.entry_list = ['Entry 1-1', 'Entry 1-2', 'Entry 1-3', 'Entry 1-4',
                           'Entry 1-5', 'Entry 1-6']
        self.table = tables.Table('Table 1')
        for e in self.entry_list:
            self.table.append(e)

    def test_Table_name(self):
        self.assertEqual(self.table.name, 'Table 1')

    def test_Table_insert_entry_string(self):
        self.assertEqual(self.table._entries, self.entry_list)

    def test_Table_len(self):
        self.assertEqual(len(self.table), 6)
        self.table.set_dice('2d3')
        self.assertEqual(len(self.table), 5)

    def test_Table_getitem_no_die(self):
        self.assertEqual(self.table[1], 'Entry 1-1')
        self.assertEqual(self.table[2], 'Entry 1-2')
        self.assertEqual(self.table[3], 'Entry 1-3')
        self.assertEqual(self.table[4], 'Entry 1-4')
        self.assertEqual(self.table[5], 'Entry 1-5')
        self.assertEqual(self.table[6], 'Entry 1-6')

    def test_Table_getitem_with_die(self):
        self.table.set_dice('2d3')
        self.assertEqual(self.table[2], 'Entry 1-1')
        self.assertEqual(self.table[3], 'Entry 1-2')
        self.assertEqual(self.table[4], 'Entry 1-3')
        self.assertEqual(self.table[5], 'Entry 1-4')
        self.assertEqual(self.table[6], 'Entry 1-5')
        with self.assertRaises(IndexError):
            self.table[1]
        with self.assertRaises(IndexError):
            self.table[7]

    def test_Table_get_entry_entries(self):
        for _ in range(1000):
            self.assertIn(self.table.get_entry(), self.entry_list)
        self.table.set_dice('2d3')
        for _ in range(1000):
            self.assertIn(self.table.get_entry(), ['Entry 1-1', 'Entry 1-2',
                                                   'Entry 1-3', 'Entry 1-4',
                                                   'Entry 1-5'])

    def test_Table_get_entry_with_table(self):
        table2 = tables.Table('Table 2', diestr='1d4')
        table2.append('Entry 2-1')
        table2.append('Entry 2-2')
        table2.append('Entry 2-3')
        table2.append('Entry 2-4')
        entry_list_2 = ['Entry 2-1', 'Entry 2-2', 'Entry 2-3', 'Entry 2-4']
        entry_list_2.extend(self.entry_list)
        self.table.append(table2)
        for _ in range(1000):
            self.assertIn(self.table.get_entry(), entry_list_2)

    def test_Table_circular_ref_error(self):
        table1 = tables.Table('Table1')
        table2 = tables.Table('Table2')
        table1.append(table2)
        table2.append(table1)
        self.assertEqual(table1.get_entry(), 'Error: Maximum Recursion')

if __name__ == '__main__':
    unittest.main()
