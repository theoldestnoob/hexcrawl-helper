# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:28:40 2019

@author: theoldestnoob
"""

import unittest

import tables


class TestTableEntry(unittest.TestCase):

    def test_TableEntry_eq(self):
        entry = tables.TableEntry('Test')
        entry2 = tables.TableEntry('Test')
        self.assertIsNot(entry, entry2)
        self.assertEqual(entry, entry2)

    def test_TableEntry_get_entry(self):
        entry = tables.TableEntry('Test')
        entry2 = entry.get_entry()
        self.assertIs(entry, entry2)


class TestTable(unittest.TestCase):

    def setUp(self):
        e_list = ['Entry 1-1', 'Entry 1-2', 'Entry 1-3', 'Entry 1-4',
                  'Entry 1-5', 'Entry 1-6']
        self.entry_list = []
        for entry in e_list:
            self.entry_list.append(tables.TableEntry(entry))
        self.table = tables.Table('Table 1')
        for e in self.entry_list:
            self.table.append(e)
        self.table.gen_table()

    def test_Table_name(self):
        table = tables.Table('Table 1')
        self.assertEqual(table.name, 'Table 1')

    def test_Table_append_entry(self):
        table = tables.Table('Table 1')
        entry = tables.TableEntry('Entry 1')
        table.append(entry)
        self.assertEqual(table._entries[0], entry)

    def test_Table_getitem_no_die(self):
        self.assertIsInstance(self.table[1], tables.TableEntry)
        self.assertIsInstance(self.table[2], tables.TableEntry)
        self.assertIsInstance(self.table[3], tables.TableEntry)
        self.assertIsInstance(self.table[4], tables.TableEntry)
        self.assertIsInstance(self.table[5], tables.TableEntry)
        self.assertIsInstance(self.table[6], tables.TableEntry)
        with self.assertRaises(IndexError):
            self.table[7]
        with self.assertRaises(IndexError):
            self.table[0]

    def test_Table_getitem_with_die(self):
        self.table.set_dice('2d3')
        self.assertIsInstance(self.table[2], tables.TableEntry)
        self.assertIsInstance(self.table[3], tables.TableEntry)
        self.assertIsInstance(self.table[4], tables.TableEntry)
        self.assertIsInstance(self.table[5], tables.TableEntry)
        self.assertIsInstance(self.table[6], tables.TableEntry)
        with self.assertRaises(IndexError):
            self.table[1]
        with self.assertRaises(IndexError):
            self.table[7]

    def test_Table_get_entry_entries(self):
        for _ in range(1000):
            self.assertIn(self.table.get_entry(), self.entry_list)
        self.table.set_dice('2d3')
        for _ in range(1000):
            self.assertIn(self.table.get_entry(), self.entry_list[:5])

    def test_Table_get_entry_with_table(self):
        table2 = tables.Table('Table 2', diestr='1d4')
        e_list_2 = ['Entry 2-1', 'Entry 2-2', 'Entry 2-3', 'Entry 2-4']
        entry_list_2 = []
        for e in e_list_2:
            entry_list_2.append(tables.TableEntry(e))
        entry_list_2.extend(self.entry_list)
        for entry in entry_list_2:
            table2.append(entry)
        self.table.append(table2)
        for _ in range(1000):
            self.assertIn(self.table.get_entry(), entry_list_2)

    def test_Table_circular_ref_error(self):
        table1 = tables.Table('Table1')
        table2 = tables.Table('Table2')
        table1.append(table2)
        table2.append(table1)
        error_entry = tables.TableEntry('Error: Recursive Tables')
        self.assertEqual(table1.get_entry(), error_entry)

    def test_Table_entry_priority(self):
        table = tables.Table('Test')
        table.append(tables.TableEntry('Prio0-1', priority=0))
        table.append(tables.TableEntry('Prio0-2', priority=0))
        table.append(tables.TableEntry('Prio5-1', priority=5))
        table.append(tables.TableEntry('Prio5-2', priority=5))
        table.append(tables.TableEntry('Prio0-3', priority=0))
        table.append(tables.TableEntry('Prio0-4', priority=0))
        table.set_dice('1d4')
        table.gen_table()
        for x in table._table:
            self.assertEqual(x.priority, 0)

    def test_Table_entry_position(self):
        table = tables.Table('Test')
        table.append(tables.TableEntry('Pos-2', pos_wt=-2))
        table.append(tables.TableEntry('Pos12', pos_wt=12))
        table.append(tables.TableEntry('Pos0', pos_wt=0))
        table.append(tables.TableEntry('Pos3', pos_wt=3))
        table.append(tables.TableEntry('Pos7', pos_wt=7))
        table.append(tables.TableEntry('Pos4', pos_wt=4))
        self.assertEqual(table[1].name, 'Pos-2')
        self.assertEqual(table[2].name, 'Pos0')
        self.assertEqual(table[3].name, 'Pos3')
        self.assertEqual(table[4].name, 'Pos4')
        self.assertEqual(table[5].name, 'Pos7')
        self.assertEqual(table[6].name, 'Pos12')

    def test_Table_entry_pos_prio(self):
        table = tables.Table('Test')
        table.append(tables.TableEntry('Pos-2', pos_wt=-2, priority=5))
        table.append(tables.TableEntry('Pos12', pos_wt=12, priority=1))
        table.append(tables.TableEntry('Pos0', pos_wt=0, priority=1))
        table.append(tables.TableEntry('Pos3', pos_wt=3, priority=10))
        table.append(tables.TableEntry('Pos7', pos_wt=7, priority=1))
        table.append(tables.TableEntry('Pos4', pos_wt=4, priority=10))
        table.set_dice('1d4')
        self.assertEqual(table[1].name, 'Pos-2')
        self.assertEqual(table[2].name, 'Pos0')
        self.assertEqual(table[3].name, 'Pos7')
        self.assertEqual(table[4].name, 'Pos12')

    def test_Table_entry_probability_simple(self):
        table = tables.Table('Test')
        table.append(tables.TableEntry('Prob0', prob_wt=0))
        table.append(tables.TableEntry('Prob0', prob_wt=0))
        table.append(tables.TableEntry('Prob1', prob_wt=1))
        table.append(tables.TableEntry('Prob1', prob_wt=1))
        table.append(tables.TableEntry('Prob-1', prob_wt=-1))
        table.append(tables.TableEntry('Prob-1', prob_wt=-1))
        self.assertEqual(table[1].name, 'Prob-1')
        self.assertEqual(table[2].name, 'Prob0')
        self.assertEqual(table[3].name, 'Prob1')
        self.assertEqual(table[4].name, 'Prob1')
        self.assertEqual(table[5].name, 'Prob0')
        self.assertEqual(table[6].name, 'Prob-1')

    def test_Table_entry_prob_smaller_table_than_entries(self):
        table = tables.Table('Test')
        table.append(tables.TableEntry('Prob0', prob_wt=0))
        table.append(tables.TableEntry('Prob0', prob_wt=0))
        table.append(tables.TableEntry('Prob1', prob_wt=1))
        table.append(tables.TableEntry('Prob1', prob_wt=1))
        table.append(tables.TableEntry('Prob-1', prob_wt=-1))
        table.append(tables.TableEntry('Prob-1', prob_wt=-1))
        table.set_dice('1d4')
        self.assertEqual(table[1].name, 'Prob0')
        self.assertEqual(table[2].name, 'Prob1')
        self.assertEqual(table[3].name, 'Prob1')
        self.assertEqual(table[4].name, 'Prob0')

    def test_Table_entry_prob_prio(self):
        table = tables.Table('Test')
        table.append(tables.TableEntry('Prob0', prob_wt=0, priority=1))
        table.append(tables.TableEntry('Prob0', prob_wt=0, priority=1))
        table.append(tables.TableEntry('Prob1', prob_wt=1, priority=1))
        table.append(tables.TableEntry('Prob1', prob_wt=1, priority=1))
        table.append(tables.TableEntry('Prob-1', prob_wt=-1, priority=0))
        table.append(tables.TableEntry('Prob-1', prob_wt=-1, priority=1))
        table.set_dice('1d4')
        self.assertIn(table[1].name, ['Prob-1', 'Prob0'])
        self.assertEqual(table[2].name, 'Prob1')
        self.assertEqual(table[3].name, 'Prob1')
        self.assertIn(table[4].name, ['Prob-1', 'Prob0'])
        self.assertNotEqual(table[1].name, table[4].name)

    def test_Table_entry_pos_prob(self):
        table = tables.Table('Sorting Test')
        print("test start")
        table.append(tables.TableEntry('11', pos_wt=1, prob_wt=1))
        table.append(tables.TableEntry('21', pos_wt=2, prob_wt=1))
        table.append(tables.TableEntry('15', pos_wt=1, prob_wt=5))
        table.append(tables.TableEntry('25', pos_wt=2, prob_wt=5))
        self.assertEqual(table[1].name, '11')
        self.assertEqual(table[2].name, '15')
        self.assertEqual(table[3].name, '25')
        self.assertEqual(table[4].name, '21')

    def test_Table_entry_pos_prob_prio(self):
        pass


if __name__ == '__main__':
    unittest.main()
