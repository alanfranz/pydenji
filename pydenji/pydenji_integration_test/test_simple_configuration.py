#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni

from .simple_app import *

from pydenji_integration_test.simple_app import SomeNetworkedClass
from pydenji.appcontext.context import AppContext
from pydenji.config.pythonconfig import Configuration, prototype, singleton


@Configuration
class MyRemoteFetchService(object):
    target_address = "somenetworkaddress"

    def network_service(self):
        return SomeService(self.networked_factory)

    @prototype
    def networked_factory(self):
        return SomeNetworkedClass(self.connector(), self.resource())

    @prototype
    def connector(self):
        return SomeConnector(self.target_address)


    @singleton.lazy
    def resource(self):
        return SomeResource


def run_basic():
    context = AppContext(MyRemoteFetchService())

    network_service = context.get_object("network_service")
