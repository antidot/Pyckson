from typing import List, Optional, Union

from pyckson.model.union import inspect_optional_typing


def test_simple_type_should_not_be_optional():
    assert inspect_optional_typing(str) == (False, type(None))
    assert inspect_optional_typing(int) == (False, type(None))


def test_simple_typing_type_should_not_be_optional():
    assert inspect_optional_typing(List[int]) == (False, type(None))


def test_optional_should_be_optional():
    assert inspect_optional_typing(Optional[str]) == (True, str)


def test_union_with_none_should_be_optional():
    assert inspect_optional_typing(Union[int, None]) == (True, int)


def test_other_unions_should_not_be_optional():
    assert inspect_optional_typing(Union[int, str]) == (False, Union[int, str])


def test_multiple_union_with_none_should_be_optional():
    assert inspect_optional_typing(Union[int, str, None]) == (True, Union[int, str])
