#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

from unittest import TestCase
import os

from pydenji.resourceloader import resource_filename_resolver



class TestFileResolver(TestCase):
    def test_resource_resolver_retrieves_filesystem_filename(self):
        resolved = resource_filename_resolver("file:/tmp/testfile")
        self.assertEquals("/tmp/testfile", resolved)

    def test_resolver_refuses_relative_file_resource(self):
        self.assertRaises(ValueError, resource_filename_resolver, "file:tmp/testfile")


class TestPackageResolver(TestCase):
    def test_resolver_retrieves_package_resource_filename(self):
        resolved = resource_filename_resolver("pkg://pydenji/test/test_resourceloader.py")
        # I don't want to use pkg_resources here because it seems not a proper
        # test just repeating what the actual implementation will be.
        # must strip Cs and Os just in case we're running from pyc or pyo.
        self.assertEquals(os.path.abspath(__file__.rstrip("co")), resolved)




