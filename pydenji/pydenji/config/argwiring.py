#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

# fetches the required args and kwargs for a function from a mapping.

from inspect import getargspec
# this won't probably work on 2.5
from itertools import izip_longest
from pydenji.lib.odict import OrderedDict

_NO_VALUE = object()


# this is getting messy. go on testing then refactor pieces out of that.
def wire(callable_obj, mapping, *additional_args, **additional_kwargs):
    # how can we support varargs and varkw?
    arg_names, varargs, varkw, defaults = getargspec(callable_obj)

    # let's determine which args can be fetched from the dict:
    current_arguments = OrderedDict()

    # additional_args and additional_kwargs should take precedence
    # on everything. clashes should be explicit.
    for arg_name, value in filter(lambda x: x[0] is not _NO_VALUE,
                        izip_longest(arg_names, additional_args,
                        fillvalue=_NO_VALUE)):
        current_arguments[arg_name] = value
        
    for kw, value in additional_kwargs.iteritems():
        if current_arguments.get(kw, _NO_VALUE) is not _NO_VALUE:
            # if it's the same value we should let'em be?
            raise TypeError, "Overlapping value for '%s' arg." % kw
        current_arguments[kw] = value

    for arg_name in arg_names:
        if current_arguments.get(arg_name, _NO_VALUE) is _NO_VALUE:
            current_arguments[arg_name] = mapping.get(arg_name, _NO_VALUE)

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



