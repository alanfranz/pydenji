#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from pkg_resources import resource_filename

from pydenji.userproperties.propertychecker import walk_for_properties_usage

class TestPropertycheckerTestCase(unittest.TestCase):

    def test_property_walk_returns_used_properties(self):
        used_properties = walk_for_properties_usage(resource_filename("pydenji", "test/propertychecker.testpy"), "PropertyUsageObject")
        self.assertEquals(set(["somekey", "otherkey"]), used_properties)
        

if __name__ == '__main__':
    unittest.main()

