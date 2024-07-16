from assertpy import assert_that

from pyckson.parsers.base import UnionParser, BasicParserWithCast, ListParser, BasicParser


class TestUnionParser:
    def test_should_parse_simple_union(self):
        parser = UnionParser([BasicParserWithCast(int)])

        result = parser.parse(5)

        assert result == 5

    def test_should_parse_list_in_union(self):
        parser = UnionParser([ListParser(BasicParserWithCast(int))])

        result = parser.parse([5, 6])

        assert result == [5, 6]

    def test_should_raise_if_parser_does_not_correspond_to_union_type(self):
        parser = UnionParser([BasicParserWithCast(int)])

        assert_that(parser.parse).raises(TypeError).when_called_with("str")

    def test_should_not_raise_if_parser_does_not_have_cls(self):
        parser = UnionParser([BasicParser(), BasicParserWithCast(int)])

        result = parser.parse(5)

        assert_that(result).is_equal_to(5)
