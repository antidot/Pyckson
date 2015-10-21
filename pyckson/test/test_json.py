from unittest import TestCase
from pyckson.json import dumps, loads
from pyckson.decorators import pyckson


class JsonHelpersTest(TestCase):
    def test_dumps(self):
        @pyckson
        class Foo:
            def __init__(self, bar: str):
                self.bar = bar

        self.assertEqual(dumps(Foo('bar')), '{"bar": "bar"}')

    def test_loads(self):
        @pyckson
        class Foo:
            def __init__(self, bar: str):
                self.bar = bar

        result = loads(Foo, '{"bar": "bar"}')

        self.assertEqual(result.bar, 'bar')
