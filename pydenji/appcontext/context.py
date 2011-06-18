#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

from pydenji.config.provider import is_object_factory, is_eager
from pydenji.appcontext.aware import AppContextAware
from pydenji.config.composite import CompositeConfig


class UnknownProviderException(Exception):
    pass

class AlreadyRegistered(Exception):
    pass

class AppContext(object):
    def __init__(self):
        self._names_providers = {}

    def register(self, name, provider):
        # TODO: limit bean names.
        if name in self._names_providers:
            raise AlreadyRegistered, "'%s' was already registered!"
        self._names_providers[name] = provider

    # we'll do this right now, in the future we might try with a ducktype-based
    # overloading.
    def register_anonymous(self, config_class):
        """
        registering a config registers a de-facto singleton bean
        with the same name as the config, AND all providers for that config.

        we want the config class to be registered, not an instance, because
        we may want or need to wire it.

        the INSTANCE will be registered with such name.
        """
        config = self._get_instance(config_class)
        # TODO: use an internal method.
        self.register(config.get_name(), lambda:config)
        for name, provider in config.get_public_providers().items():
            self.register(name, provider)

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








