#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

from unittest import TestCase
import os

from pydenji.resourceloader import resourceloader



class TestFileResourceLoader(TestCase):
    def test_resourceloader_retrieves_file_resource(self):
        resolved = resourceloader("file:/tmp/testfile")
        self.assertEquals("/tmp/testfile", resolved)

    def test_resourceloader_refuses_relative_file_resource(self):
        self.assertRaises(ValueError, resourceloader, "file:tmp/testfile")


class TestPackageResourceLoader(TestCase):
    def test_resourceloader_retrieves_file_resource(self):
        resolved = resourceloader("pkg://pydenji/test/test_resourceloader.py")
        # I don't want to use pkg_resources here because it seems not a proper
        # test just repeating what the actual implementation will be.
        # must strip Cs and Os just in case we're running from pyc or pyo.
        self.assertEquals(os.path.abspath(__file__.rstrip("co")), resolved)




