from unittest.case import TestCase

from pyckson import parse
from pyckson.decorators import no_camel_case, pyckson, namerule, rename
from pyckson.serializer import serialize


class NameRulesTest(TestCase):
    def test_no_camel_case(self):
        @pyckson
        @no_camel_case
        class Foo:
            def __init__(self, foo_bar: str):
                self.foo_bar = foo_bar

        foo = Foo('foo')
        self.assertEqual(serialize(foo), {'foo_bar': 'foo'})

    def test_custom_name_rule(self):
        def my_rule(python_name):
            return 'foo' + python_name

        @pyckson
        @namerule(my_rule)
        class Foo:
            def __init__(self, bar: str):
                self.bar = bar

        foo = Foo('foo')
        self.assertEqual(serialize(foo), {'foobar': 'foo'})

    def test_rename_rule(self):
        @pyckson
        @rename(foo='_foo', bar='bar_')
        class Foo:
            def __init__(self, foo: str, bar: str):
                self.foo = foo
                self.bar = bar

        foo = Foo('foo', 'bar')
        self.assertEqual(serialize(foo), {'_foo': 'foo', 'bar_': 'bar'})
        foo = parse(Foo, {'_foo': 'foo', 'bar_': 'bar'})
        self.assertEqual(foo.foo, 'foo')
        self.assertEqual(foo.bar, 'bar')

    def test_rename_and_no_camel_case(self):
        @pyckson
        @rename(foo='_foo')
        @no_camel_case
        class Foo:
            def __init__(self, foo: str, bar_bar: str):
                self.foo = foo
                self.bar_bar = bar_bar

        foo = Foo('foo', 'bar')
        self.assertEqual(serialize(foo), {'_foo': 'foo', 'bar_bar': 'bar'})
