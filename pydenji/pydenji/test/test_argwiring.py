#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

import unittest

from pydenji.config.argwiring import wire, _NO_VALUE

def func_to_wire(pos1, pos2, kw1="a", kw2="b"):
    return (pos1, pos2, kw1, kw2)

class  TestArgwiring(unittest.TestCase):
    def test_all_nonvariable_arguments_can_be_wired_from_dictionary(self):
        d = { "pos1":1, "pos2": 2, "kw1": 3, "kw2": 4 }
        obj = wire(func_to_wire, d)
        self.assertEquals( (1,2,3,4), obj )

    def test_missing_args_from_mapping_are_fetched_from_defaults(self):
        d = { "pos1":1, "pos2": 2, "kw1": 3 }
        obj = wire(func_to_wire, d)
        self.assertEquals( (1,2,3,"b"), obj )

    def test_error_raised_if_required_args_cant_be_completed(self):
        d = { "pos1":1, }
        self.assertRaises(TypeError, wire, func_to_wire, d )

    def test_positional_additional_arguments_have_precedence(self):
        d = { "pos1":1, "pos2": 2, "kw1": 3 }
        obj = wire(func_to_wire, d, "x")
        self.assertEquals( ("x", 2 ,3,"b"), obj)

    def test_positional_additional_kw_arguments_have_precedence(self):
        d = { "pos1":1, "pos2": 2, "kw1": 3 }
        obj = wire(func_to_wire, d, pos2="y")
        self.assertEquals( (1, "y" ,3, "b"), obj)

    def test_positional_and_kw_arguments_dont_clash(self):
        d = { "pos1":1, "pos2": 2, "kw1": 3 }
        obj = wire(func_to_wire, d, 5, pos2="y")
        self.assertEquals( (5, "y" ,3, "b"), obj)

    def test_overlapping_args_and_kwargs_raise_error(self):
        d = { "pos1":1, "pos2": 2, "kw1": 3 }
        #self.assertRaises(TypeError, wire, func_to_wire, d, 5, pos1="5")

    def test_too_many_args_raise_typeerror(self):
        d = { "pos1":1, "pos2": 2, "kw1": 3 }
        self.assertRaises(TypeError, wire, func_to_wire, d, 1,2,3,4,5)

    def test_argument_positions_do_not_get_mismatched(self):
        self.assertRaises(TypeError, wire, func_to_wire, {}, 1, kw1=1, kw2=4)

        
if __name__ == '__main__':
    unittest.main()

