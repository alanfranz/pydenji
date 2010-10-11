#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

import unittest
from pydenji.userproperties.mapping import map_properties_to_obj, ConfigObjPropertyMapper
from pydenji.userproperties.mapping import inject_properties_from




class MockConfig2(object):
    def __init__(self, props):
        self.props = props.verify(raise_errors=True)

    def mymethod(self):
        some = self.props["missingkey"]

class  Test_configobj_mappingTestCase(unittest.TestCase):
    example_config = """
    # for an object
    [object]
    property1="a"
    property2="b"

    # when are they set? automagically? explicitly? they can be both set?
    # probably: if property1 exists, then it is set, otherwise it isn't, and
    # everything is available in the config as well.

    # do I want to deliver something to a config itself?
    [SomeConfig]
    prop1="x"

    # placeholders resolution? there're no java properties here...
    # but my config REALLY needs something from outside.
    # special placeholder and if not resolved crash after instantiation?

    e.g. something like

    @Configuration
    class MyConfig(object):
        someprop = MustBeSet()

        ...

    


    """
    class TestObj(object):
        property1 = None


    def test_dictmapper_maps_existent_properties(self):
        o = self.TestObj()
        map_properties_to_obj({"property1": 5}, o)
        self.assertEquals(5, o.property1)


    def test_dictmapper_forbids_mapping_non_existent_properties_by_default(self):
        o = self.TestObj()
        self.assertRaises(ValueError, map_properties_to_obj,
            {"property2": 5}, o)

    def test_dictmapper_allows_mapping_non_existent_properties_if_asked(self):
        o = self.TestObj()
        map_properties_to_obj({"property2": 5}, o, map_nonexistent=True)
        self.assertEquals(5, o.property2)

    def test_mapping_properties_to_config(self):
        class MockConfig(object):
            property1 = 1

        
        config = ConfigObjPropertyMapper(
        ["[MockConfig]", "property1=123"]
        )(MockConfig)()
        self.assertEquals(123, config.property1)

    def disabletest_properties_are_injected_as_keyword(self):
        class MockConfig1(object):
            def __init__(self, props):
                self.props = props
                
        config = inject_properties_from(["[MockConfig1]", "property1=123"])(MockConfig1)()
        self.assertEquals(123, config.props["property1"])

    def disabletest_properties_raises_error_on_unset_properties(self):
        config = inject_properties_from(["[MockConfig2]", "property1=123"])(MockConfig2)
        #self.assertRaises(ValueError, config)













