#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.
from configobj import ConfigObj
from pydenji._aop.intercept import intercept

class override_with(object):
    def __init__(self, configobj_source):
        self._co = ConfigObj(configobj_source, unrepr=True)

    def __call__(self, config_cls):
        for section_name in self._co.sections:
            def section_interceptor(context):
                o = context.proceed()
                for k, v in self._co[section_name].items():
                    setattr(o, k, v)
                return o
            config_cls = intercept(config_cls, section_name, section_interceptor)

        return config_cls
