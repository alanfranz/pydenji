#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

from unittest import TestCase

from pydenji.config.composite import CompositeConfig
from pydenji.config.pythonconfig import prototype, singleton

class FirstConfig(object):
    @singleton
    def first(self):
        return 1

class SecondConfig(object):
    @prototype
    def second(self):
        return 2

class TestCompositeConfig(TestCase):

    def test_composite_config_merges_input_configs(self):
        first = FirstConfig()
        second = SecondConfig()
        second.second()
        
        composite = CompositeConfig((first, second))

        self.assertEquals(1, composite.first())
        self.assertEquals(2, composite.second())



