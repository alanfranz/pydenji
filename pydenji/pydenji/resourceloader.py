#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

# TBD: something to get consistent access to resources, just like
# springs own classpath/file/url etc. parser.
# check:
# how to work with pkg_resources Requirement classes
# how to work with pkg_resources split packages, e.g. those using namespace_packages
# how will this play along distutils2 and its pkgutil.open()

from urlparse import urlparse

from pkg_resources import resource_filename


# this currently more a resourcelocator than a resourceloader. 

# do we need this?
class Resource(object):

    # will the stream be open for reading or for writing?
    # by default I think we'll just support reading streams.
    # binary or not?
    # too complex?
    # check what Spring does.
    def get_stream(self, mode):
        raise NotImplementedError, "Not yet implemented."

    @property
    def filename(self):
        raise NotImplementedError, "Not yet implemented."

def file_uri_resolver(parsed_uri):
    if not parsed_uri.path.startswith("/"):
        raise ValueError, "Relative paths are not supported."
    if parsed_uri.netloc:
        raise ValueError, "Netloc in file scheme is unsupported."
    return parsed_uri.path

def package_uri_resolver(parsed_uri):
    return resource_filename(parsed_uri.netloc, parsed_uri.path)

# todo: support hooks for different schemes?
supported_schemes = {
    "file" : file_uri_resolver,
    "pkg": package_uri_resolver,
}


# should it break if resource does not exist?
# maybe optionally? a differenct factory? readresourceloader, writeresourceloader,
# mayberesourceloader?
def resourceloader(resource_uri):
    parsed = urlparse(resource_uri)
    if parsed.scheme not in supported_schemes:
        raise TypeError, "Scheme '%s' is unsupported" % parsed.scheme

    return supported_schemes[parsed.scheme](parsed)





    


