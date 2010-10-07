#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2010 Alan Franzoni.

import compiler

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


def walk_for_properties_usage(filename, object_name):
    ast = compiler.parseFile(filename)
    visitor = ClassVisitor(object_name)
    compiler.visitor.walk(ast, visitor)
    return visitor.accumulator


