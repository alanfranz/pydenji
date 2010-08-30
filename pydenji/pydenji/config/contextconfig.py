#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni

from pydenji.appcontext.aware import is_appcontext_aware
from pydenji.config.pythonconfig import Configuration
from pydenji.config.pythonconfig import singleton


def GlobalConfiguration(cls, configure_with=singleton, suffix="GlobalConfiguration"):
    """
    Just like Configuration, but any unfound factory will be looked up in the app context.
    """
    
    ConfigClass = Configuration(cls, configure_with, suffix)
    # it might be appcontext aware but we
    # could not detect it without ABCs...
    # TODO: think about that.
    if is_appcontext_aware(ConfigClass):
        # just return it, it's already got whatever it needs. (maybe?)
        # TODO: let's think if this can do any harm.
        return ConfigClass

    configured_dict = {}

    # TODO: do we need to wrap this in a dontconfigure decorator?
    def set_app_context(self, context):
        self._pydenji__app_context = context

    configured_dict["set_app_context"] = set_app_context
    configured_dict["_pydenji__app_context"] = None

    def __getattr__(self, attr):
        try:
            return lambda *args, **kwargs: self._pydenji__app_context.get_object(attr, *args, **kwargs)
        except:
            # TODO: better error interception! just intercept what we
            # need to handle.
            raise KeyError, "'%s' object has no attribute '%s'" % (self, attr)

    configured_dict["__getattr__"] = __getattr__

    cls_type = type(cls)
    return cls_type(cls.__name__ + suffix, (ConfigClass, ), configured_dict)
