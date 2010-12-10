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

      



if __name__ == '__main__':
    unittest.main()

