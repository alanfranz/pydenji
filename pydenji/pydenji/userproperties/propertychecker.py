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

    def visitGetattr(self, node):
        print node

    def visitSubscript(self, node):
        n = compiler.visitor.walk(node, GetattrVisitor())
        if n.found_node:
            print dir(node)
            if (node.flags == compiler.consts.OP_APPLY):
                # use a ConstWalker and so something if it's a const.
                print dir(node.subs[0])





class ClassVisitor(compiler.visitor.ASTVisitor):
    classname = "SomeClass"
    def visitClass(self, node):
        #print node
        if node.name == self.classname:
            compiler.visitor.walk(node, PropVisitor())


ast = compiler.parseFile("/tmp/parsed.py")
compiler.visitor.walk(ast, ClassVisitor())

"""

class SomeClass(object):
    def mything(self):
        used = self.props["helloworld"]

"""