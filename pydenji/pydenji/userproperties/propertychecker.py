#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

import compiler
import os
from inspect import getsourcefile
from inspect import getsource

class GetattrVisitor(compiler.visitor.ASTVisitor):
    propattrname = "props"

    found_node = False

    def visitGetattr(self, node):
        if node.attrname == self.propattrname:
            self.found_node = True

class SubscriptVisitor(compiler.visitor.ASTVisitor):
    pass

class PropVisitor(compiler.visitor.ASTVisitor):
    propattrname = "props"

    def __init__(self, accumulator):
        self.accumulator = accumulator

    def visitGetattr(self, node):
        print node

    def visitSubscript(self, node):
        n = compiler.visitor.walk(node, GetattrVisitor())
        if n.found_node:
            if (node.flags == compiler.consts.OP_APPLY):
                    self.accumulator.add(node.subs[0].value)

class ClassVisitor(compiler.visitor.ASTVisitor):
    def __init__(self, classname):
        compiler.visitor.ASTVisitor.__init__(self)
        self.classname = classname
        self.accumulator = set()
    
    def visitClass(self, node):
        if node.name == self.classname:
            compiler.visitor.walk(node, PropVisitor(self.accumulator))


def _get_actual_file_to_parse(filename):
    # whenever using introspection it might happen that we get .pyc or .pyo files.
    # but we can't parse those, we need the actual source. Check what happens with more recent
    # python versions and the new pyc cache.
    if filename.endswith(".pyc") or filename.endswith(".pyo"):
        return filename[:-3] + "py"
    return filename




def walk_for_properties_usage(ast, object_name):
    # very naive! won't work if some inheritance occurs.
    visitor = ClassVisitor(object_name)
    compiler.visitor.walk(ast, visitor)
    return visitor.accumulator

def get_used_properties(obj):
    cls = obj.__class__
    return walk_source_for_properties_usage(getsource(cls), cls.__name__)

def walk_file_for_properties_usage(filename, object_name):
    return walk_for_properties_usage(compiler.parseFile(_get_actual_file_to_parse(filename)), object_name)

def walk_source_for_properties_usage(src, object_name):
    return walk_for_properties_usage(compiler.parse(src), object_name)



