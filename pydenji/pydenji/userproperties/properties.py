#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.


# this is just an empty container right now.

from copy import deepcopy
from inspect import getframe

class _FrozenDict(object):
    def __init__(self, d):
        self._d = deepcopy(d)

    def __getitem__(self, item):
        return self._d[item]
    
    def verify(self, raise_errors=False):
        return self


def UserProperties(property_mapping):
    return _FrozenDict(property_mapping)




