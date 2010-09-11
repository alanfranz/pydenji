#!/usr/bin/env python
# -*- coding: utf-8 -*-

_NO_VALUE = object()

def map_properties_to_obj(d, obj, map_nonexistent=False):
    for key, value in d.iteritems():
        if (getattr(obj, key, _NO_VALUE) is _NO_VALUE) and not map_nonexistent:
            raise ValueError, "Object '%s' hasn't got a '%s' attribute" % (obj, key)
        setattr(obj, key, value)
    return obj
