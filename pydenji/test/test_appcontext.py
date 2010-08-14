#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni

from unittest import TestCase

from pydenji.appcontext import AppContext, is_appcontext_aware
from pydenji.config.pythonconfig import singleton
from pydenji.config.pythonconfig import Configuration

class TestAppContext(TestCase):
    def test_appcontext_allows_retrieving_by_name(self):
        @Configuration
        class MockConf(object):
            @singleton
            def something(self):
                return 1

        context = AppContext(MockConf())
        something = context.get_object("something")
        self.assertEquals(1, something)

    def test_appcontext_fetches_objects_eagerly_when_required(self):
        c = []
        @Configuration
        class MockConf(object):
            @singleton
            def something(self):
                c.append(True)
             

        conf = MockConf()
        context = AppContext(conf)
        self.assertEquals([True], c)

    def test_appcontext_fetches_objects_lazily_when_required(self):
        c = []
        @Configuration
        class MockConf(object):
            @singleton.lazy
            def something(self):
                c.append(True)


        conf = MockConf()
        context = AppContext(conf)
        self.assertEquals([], c)

    def test_appcontext_gets_injected_on_aware_objects(self):
        # TODO: think whether we need to use an ABC instead or as well.
        class AppAwareObject(object):
            app_context = None
            
            def set_app_context(self, context):
                self.app_context = context

        @Configuration
        class MockConf(object):
            @singleton
            def appcontextaware(self):
                return AppAwareObject()


        context = AppContext(MockConf())
        aware = context.get_object("appcontextaware")
        self.assertTrue(context is aware.app_context, "context wasn't injected correctly!")





