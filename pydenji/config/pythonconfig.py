# -*- coding: utf-8 -*-
# (C) 2011 Alan Franzoni.

from ducktypes.ducktype import DuckABCMeta

from pydenji.config.provider import dontconfigure, is_object_factory

class Configuration(object):
    __metaclass__ = DuckABCMeta
    # TODO: we might stop people from using get_... names?

    def get_public_providers(self):
        """
        @rtype dict name:provider
        """
        names_providers = {}
        for attr in filter(lambda a: not a.startswith("_"), dir(self)):
            value = getattr(self, attr)
            if is_object_factory(value):
                names_providers[attr] = value
        return names_providers

    @property
    def get_name(self):
        return self.__class__.__name__



