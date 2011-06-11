#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

from pydenji.config.provider import is_object_factory, is_eager
from pydenji.appcontext.aware import AppContextAware
from pydenji.config.composite import CompositeConfig


class UnknownProviderException(Exception):
    pass


class AppContext(object):
    def __init__(self):
        self._names_providers = {}
#        pass

#                 *configurations):
#        self._names_factories = {}
#        for conf in configurations:
#            self.register(conf.__name__, conf)
        #self._start(self._names_factories)

    def register(self, name, provider):
        # TODO: what to do if there's already a provider for that name?
        self._names_providers[name] = provider
        # this is something we do for configs, makes no sense for other
        # object, we'd probably MUCH better create an interface for configuration
        # objects.
        #names_factories = self._get_all_factories(provider)
        # TODO: this does not check for overwrites, should it?
        #self._names_factories.update(names_factories)

    def __contains__(self, key):
        return key in self._names_providers

    def __iter__(self):
        return self._names_providers.iterkeys()


    def provide(self, name, *args, **kwargs):
        try:
            provider = self._names_providers[name]
        except KeyError:
            raise UnknownProviderException, "No provider was configured for '%s'" % name
        return self._get_instance(provider, *args, **kwargs)
    
    def start(self):
        for provider in self._names_providers.values():
            if is_eager(provider):
                self._get_instance(provider)

    def _get_instance(self, factory, *args, **kwargs):
        # this way the set_app_context() method will be called multiple times,
        # even though the object is a singleton. While it should make no harm,
        # we should think about it, might it do any harm?
        obj = factory(*args, **kwargs)
        if isinstance(obj, AppContextAware):
            obj.set_app_context(self)
        return obj








