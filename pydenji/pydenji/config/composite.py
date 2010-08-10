#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni
from pydenji.config.pythonconfig import is_object_factory

class CompositeConfig(object):
    def __init__(self, configs):
        # this resembles appcontext method.
        # TODO: check whether we could refactor it someway.
        for config in configs:
            for attr in dir(config):
                value = getattr(config, attr)
                if is_object_factory(value):
                    setattr(self, attr, value)

        
    
    