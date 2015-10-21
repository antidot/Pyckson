from unittest import TestCase
from pyckson import pyckson, serialize

from pyckson.builders import PycksonModelBuilder


class Foo:
    def __init__(self, foo: 'Foo'):
        pass


class Bar:
    def __init__(self, quz: 'Quz'):
        pass


class Quz:
    def __init__(self, bar: 'Bar'):
        pass


@pyckson
class Fail:
    def __init__(self, bar: 'Toto'):
        self.bar = bar


class TestForwardDeclarations(TestCase):
    def test_should_parse_recursive(self):
        model = PycksonModelBuilder(Foo).build_model()
        self.assertEqual(model.get_attribute(python_name='foo').attr_type, Foo)

    def test_should_parse_indirect_recursive(self):
        model = PycksonModelBuilder(Bar).build_model()
        self.assertEqual(model.get_attribute(python_name='quz').attr_type, Quz)

        model = PycksonModelBuilder(Quz).build_model()
        self.assertEqual(model.get_attribute(python_name='bar').attr_type, Bar)

    def test_should_raise_error_on_unresolvedtype(self):
        with self.assertRaises(TypeError):
            serialize(Fail('toto'))
