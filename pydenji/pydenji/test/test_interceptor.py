# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest

from pydenji._aop.intercept import intercept

class TestInterception(unittest.TestCase):
    class MyTestClass(object):
        clsattr = 12

        def __init__(self, arg, clsattr=5):
            self.arg = arg
            self.clsattr = clsattr

        def method(self, value):
            return self.arg + value

        @classmethod
        def class_method(cls, value):
            return cls.clsattr + value

        @staticmethod
        def static_method(value):
            return 7 + value

    # TODO: split those tests into multiple tests!
    def test_init_interception(self):
        def init_interceptor(context):
            self.assertRaises(AttributeError, getattr, context.args[0], "arg")
            context.proceed()
            instance = context.args[0]
            instance.other_arg = 5
           

        intercepted = intercept(self.MyTestClass, "__init__", init_interceptor)
        test_obj = intercepted(3)
        self.assertEquals(3, test_obj.arg)
        self.assertEquals(5, test_obj.other_arg)


    def test_instancemethod_interception(self):
        def method_interceptor(context):
            value = context.proceed()
            return value * 4

        intercepted = intercept(self.MyTestClass, "method", method_interceptor)
        test_obj = intercepted(3)
        self.assertEquals((3 + 5) * 4, test_obj.method(5))

    # TODO: refactor and split in two.
    def test_class_method_interception(self):
        def class_method_interceptor(context):
            value = context.proceed()
            return value * 2


        intercepted = intercept(self.MyTestClass, "class_method", class_method_interceptor)
        test_obj = intercepted
        self.assertEquals((5 + 12) * 2, test_obj.class_method(5))
        test_obj = intercepted(0)
        self.assertEquals((5 + 12) * 2, test_obj.class_method(5))


    # TODO: split test in two parts.
    def test_static_method_interception(self):
        def static_method_interceptor(context):
            value = context.proceed()
            return value * 2


        intercepted = intercept(self.MyTestClass, "static_method", static_method_interceptor)
        test_obj = intercepted
        self.assertEquals(( 5 + 7) *2, test_obj.static_method(5))
        test_obj = intercepted(0)
        self.assertEquals((5 + 7) * 2, test_obj.static_method(5))


