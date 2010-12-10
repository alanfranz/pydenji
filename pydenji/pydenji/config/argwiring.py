#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

# fetches the required args and kwargs for a function from a mapping.

from inspect import getargspec

_NO_VALUE = object()

def wire(callable_obj, mapping, *additional_args, **additional_kwargs):
    args, varargs, varkw, defaults = getargspec(callable_obj)

    # let's determine which args can be fetched from the dict:
    call_args = []
    for arg in args:
        call_args.append(mapping.get(arg, _NO_VALUE))

    return callable_obj(*call_args)



