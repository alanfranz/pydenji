#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

# fetches the required args and kwargs for a function from a mapping.

from inspect import getargspec

def wire(callable_obj, mapping, *call_args, **call_kwargs):
    all_arg_names, ignore, ignore, ignore  = getargspec(callable_obj)

    # we might want to fetch something from our mapping to fill in
    # named arguments that were not passed, without overwriting
    # anything that was passed as a kw arg.
    for arg_name in all_arg_names[len(call_args):]:
        if arg_name in mapping:
            call_kwargs.setdefault(arg_name, mapping[arg_name])

    return callable_obj(*call_args, **call_kwargs)
