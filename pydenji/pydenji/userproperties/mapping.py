#!/usr/bin/env python
# -*- coding: utf-8 -*-

_NO_VALUE = object()

def map_properties_to_obj(d, obj):
    for key, value in d.iteritems():
        if getattr(obj, key, _NO_VALUE) is _NO_VALUE:
            raise ValueError, "Object '%s' hasn't got a '%s' attribute" % (obj, key)
        setattr(obj, key, value)
    return obj
