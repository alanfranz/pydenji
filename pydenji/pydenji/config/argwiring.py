#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

# fetches the required args and kwargs for a function from a mapping.

from inspect import getargspec
from pydenji.lib.odict import OrderedDict

_NO_VALUE = object()


def wire(callable_obj, mapping, *additional_args, **additional_kwargs):
    args, varargs, varkw, defaults = getargspec(callable_obj)

    # let's determine which args can be fetched from the dict:
    current_arguments = OrderedDict()

    for arg in args:
        current_arguments[arg] = mapping.get(arg, _NO_VALUE)

    # complete missing args with default args
    for default_value, (arg_name, current_value) in zip(reversed(defaults),
                reversed(current_arguments.items())):
        if current_value is _NO_VALUE:
            current_arguments[arg_name] = default_value

    # if there's still any _NO_VALUE, we're in trouble. let's collect
    # which keys are missing in order to convey a good error message.
    missing_keys = "','".join([key for key, value in current_arguments.iteritems()
        if value is _NO_VALUE])
    if missing_keys:
        raise TypeError, ("Could not wire '%s':\n"
            "Can't determine values for the following args: '%s'\n" % (
                callable_obj, missing_keys))

    return callable_obj(*current_arguments.values())



