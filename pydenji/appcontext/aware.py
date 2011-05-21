#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni

from abc import abstractmethod
from ducktypes.ducktype import DuckABCMeta


def is_appcontext_aware(obj):
    # TODO: should we check for callability as well?
    if getattr(obj, "set_app_context", None) is not None:
        return True
    return False

class AppContextAware(object):
    __metaclass__ = DuckABCMeta

    @abstractmethod
    def set_app_context(self, context):
        pass

