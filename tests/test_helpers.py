from typing import Union
from unittest import TestCase

from pyckson.helpers import camel_case_name, is_union_annotation


class CamelCaseNameTest(TestCase):
    def test_should_do_nothing_on_simple_names(self):
        self.assertEqual(camel_case_name('foo'), 'foo')

    def test_should_camel_case_when_there_is_an_underscore(self):
        self.assertEqual(camel_case_name('foo_bar'), 'fooBar')


def test_should_detect_union_annotation():
    annotation = Union[str, int]

    is_union = is_union_annotation(annotation)

    assert is_union
