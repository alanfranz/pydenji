#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

# fetches the required args and kwargs for a function from a mapping.

from pydenji._inspect.getcallableargspec import getargspec


# important notice: every "dynamic proxy" function accepting variable positional
# and keyword arguments might disrupt wiring!

def wire(callable_obj, mapping, *call_args, **call_kwargs):
    print type(callable_obj), callable_obj
    all_arg_names, ignore, ignore, ignore = getargspec(callable_obj)

    # we might want to fetch something from our mapping to fill in
    # named arguments that were not passed, without overwriting
    # anything that was passed as a kw arg.
    for arg_name in all_arg_names[len(call_args):]:
        if arg_name in mapping:
            call_kwargs.setdefault(arg_name, mapping[arg_name])

    return callable_obj(*call_args, **call_kwargs)

