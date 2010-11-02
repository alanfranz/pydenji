#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

from unittest import TestCase
import os
from tempfile import NamedTemporaryFile
from tempfile import mkdtemp
from shutil import rmtree

from pydenji.resourceloader import resource_filename_resolver
from pydenji.resourceloader import ReadResource
from pydenji.resourceloader import OverwritingWriteResource
from pydenji.resourceloader import AppendingWriteResource
from pydenji.resourceloader import NewFileWriteResource



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


class TestResourceLoader(TestCase):
    # think: existing == accessible, or not?
    def setUp(self):
        temp = NamedTemporaryFile()
        temp.write("hello")
        temp.flush()
        self.temp = temp

    def tearDown(self):
        self.temp.close()
            
    def test_reading_loaded_resource(self):
        # what would I like for this?
        # - since it's a ReadResource, it should raise an exception if it does not
        # exists or if we're unable to read it because of permission issues.
        # - I should be able to specify additional data for the stream(), e.g. b and +
        # the interface can be limited to stream() & filename

        content = ReadResource("file://" + self.temp.name).stream().read()
        self.assertEquals("hello", content)

    def test_error_not_existing_resource(self):
        # what would I like for this?
        # - since it's a ReadResource, it should raise an exception if it does not
        # exists or if we're unable to read it because of permission issues.
        # - I should be able to specify additional data for the stream(), e.g. b and +
        # the interface can be limited to stream() & filename

        self.assertRaises(ValueError,
            ReadResource, "file://" + "/dmfsdmfdksm/kmfdskmfksdmfksdmfdksm")

    def test_error_unaccessible_resource(self):
        os.chmod(self.temp.name, 0)
        self.assertRaises(ValueError,
            ReadResource, "file://" + self.temp.name)


class TestWriteResource(TestCase):
    def setUp(self):
        self.tempdir = mkdtemp()

    def tearDown(self):
        rmtree(self.tempdir)

    def test_if_file_exists_but_is_not_writeable_error_raised(self):
        f = open(self.tempdir + os.sep + "newfile", "w")
        f.close()
        os.chmod(self.tempdir + os.sep + "newfile", 0)
        self.assertRaises(ValueError, OverwritingWriteResource, "file://" + self.tempdir + os.sep + "newfile")
        
    def test_overwriting_resource_allows_writing_if_file_does_not_exist(self):
        resource = OverwritingWriteResource("file://" + self.tempdir + os.sep + "newfile")

    def test_overwriting_resource_allows_writing_if_file_exists(self):
        f = open(self.tempdir + os.sep + "newfile", "w")
        f.write("abc")
        f.flush()
        resource = OverwritingWriteResource("file://" + self.tempdir + os.sep + "newfile")

    def test_overwriting_allows_writing_to_resource(self):
        resource = OverwritingWriteResource("file://" + self.tempdir + os.sep + "newfile")
        stream = resource.stream()
        stream.write("abc")
        stream.close()

        f = open(self.tempdir + os.sep + "newfile")
        self.assertEquals("abc", f.read())

    def test_appending_writing_resource_appends_if_file_exists(self):
        f = open(self.tempdir + os.sep + "newfile", "w")
        f.write("asd")
        f.close()

        resource = AppendingWriteResource("file://" + self.tempdir + os.sep + "newfile")
        stream = resource.stream()
        stream.write("fgh")
        stream.close()
        
        f = open(self.tempdir + os.sep + "newfile", "r")
        self.assertEquals("asdfgh", f.read())

    def test_appending_writing_resource_creates_if_file_does_not_exist(self):
        resource = AppendingWriteResource("file://" + self.tempdir + os.sep + "newfile")
        stream = resource.stream()
        stream.write("fgh")
        stream.close()

        f = open(self.tempdir + os.sep + "newfile", "r")
        self.assertEquals("fgh", f.read())

    def test_newfile_write_resource_creates_if_file_does_not_exist(self):
        resource = NewFileWriteResource("file://" + self.tempdir + os.sep + "newfile")

    def test_newfile_write_resource_raises_error_if_file_exists(self):
        f = open(self.tempdir + os.sep + "newfile", "w")
        f.write("asd")
        f.close()

        self.assertRaises(ValueError, NewFileWriteResource, "file://" + self.tempdir + os.sep + "newfile")


#
    def disabletest_maybe_resource(self):
        # sometimes we're uncertain whether a certain read resource exists
        # and we don't want to throw an exception if it doesn't.
        # the interface is slightly different and it's clear that it's a factory

        # should we call this firstExistingResource?
        maybe, resource = maybeReadResource("gianni", "pinotto", "giannina",
                                        additional_mode="...")
        # return the first existing resource between those that were passed.
        # if at least one exists, maybe is true and resource is a ReadResource;
        # if all resources get checked and none exists, maybe is False and resource
        # is None






