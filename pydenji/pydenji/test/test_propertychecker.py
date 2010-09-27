#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from pydenji.userproperties.propertychecker import walk_for_properties_usage

class PropertyUsageObject(object):
    def somemethod(self):
        self.dosomething = self.props["somekey"]

    def othermethod(self):
        s = object(self.props["otherkey"])

class TestPropertycheckerTestCase(unittest.TestCase):

    def test_property_walk_returns_used_properties(self):
        used_properties = walk_for_properties_usage(__file__, "PropertyUsageObject")
        self.assertEquals(set(["somekey", "otherkey"]), used_properties)
        

if __name__ == '__main__':
    unittest.main()

