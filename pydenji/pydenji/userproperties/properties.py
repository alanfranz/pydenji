#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.


# this is just an empty container right now.

# possible improvements include defining __contains__ and something to enumerate its properties.
from copy import deepcopy
# TODO: improve this very basic class. let's think if we want to depend on python 2.6.
class _FrozenDict(object):
    def __init__(self, d):
        self._d = deepcopy(d)

    def __getitem__(self, item):
        return self._d[item]


def UserProperties(property_mapping):
    return _FrozenDict(property_mapping)




