#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.
from inspect import getabsfile
from compiler import parseFile
from configobj import ConfigObj
from pydenji.userproperties.properties import UserProperties


_NO_VALUE = object()

def map_properties_to_obj(d, obj, map_nonexistent=False):
    for key, value in d.iteritems():
        # TODO: this is a simple check, what if "value" is a method?
        if (getattr(obj, key, _NO_VALUE) is _NO_VALUE) and not map_nonexistent:
            raise ValueError, "Object '%s' hasn't got a '%s' attribute" % (obj, key)
        setattr(obj, key, value)
    return obj

#TODO: think about a real use case for this class :-/ we might just kill it.
class ConfigObjPropertyMapper(object):
    def __init__(self, configobj_source):
        self._co = ConfigObj(configobj_source, unrepr=True)

    def __call__(self, config_cls):
        # FIXME: we'll need a utility "aop" function to intercept calls.
        original_init = config_cls.__init__
        def new_init(new_self, *args, **kwargs):
            original_init(new_self, *args, **kwargs)
            # TODO: should we let the config name to be set explicitly?
            # TODO: name is changed by our decorator right now, maybe it shouldn't.
            map_properties_to_obj(self._co[config_cls.__name__], new_self)
            
        config_cls.__init__ = new_init
        return config_cls

class inject_properties_from(object):
    def __init__(self, configobj_source, target_kwarg="props"):
        self._co = ConfigObj(configobj_source, unrepr=True)
        self._target = target_kwarg
        
    def __call__(self, config_cls):
        original_init = config_cls.__init__
        def new_init(new_self, *args, **kwargs):
            # do we need to do something like an override?
            if self._target in kwargs:
                raise ValueError, "'%s' kw args was supplied already!"
            props = UserProperties(self._co[config_cls.__name__])
            kwargs[self._target] = props
            original_init(new_self, *args, **kwargs)


        config_cls.__init__ = new_init
        return config_cls

    def _get_used_properties(self, cls):
        ast = parseFile(getabsfile(cls))






