#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

# fetches the required args and kwargs for a function from a mapping.

from inspect import getargspec
# this won't probably work on 2.5
from itertools import izip_longest
from pydenji.lib.odict import OrderedDict

class _NoValue(object):
    def __str__(self):
        return "<NoValue>"
_NO_VALUE = _NoValue

class _Argument(object):
    def __init__(self, name, value=_NO_VALUE):
        self.name = name
        self.value = value

    def __repr__(self):
        return "Arg( %s -> %s )" % (self.name, self.value)

def wire(callable_obj, mapping, *call_args, **call_kwargs):
    all_arg_names, ignore, ignore, ignore  = getargspec(callable_obj)

    # we want to use at most len(call_args) positional arguments; everything else
    # works better if handled as a kw argument.
    positional_args = OrderedDict([(name, _Argument(name, value)) for value, name
        in zip(call_args, all_arg_names)])

    # fetch from mapping whatever was not set so far, but never overwrite
    # what was not set.
    for arg_name in all_arg_names[len(positional_args):]:
        if arg_name in mapping:
            call_kwargs.setdefault(arg_name, mapping[arg_name])

    # collect positional arguments headed to variable positional arguments
    var_call_args = list(call_args[len(positional_args):])

    return callable_obj(*([argument.value for argument in positional_args.values()] +
            var_call_args), **call_kwargs)
