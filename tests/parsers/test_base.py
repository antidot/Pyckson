from assertpy import assert_that

from pyckson.parsers.base import ParserException, SetParser, UnionParser, BasicParserWithCast, ListParser, BasicParser


class TestBasicParserWithCast:
    def test_should_handle_simple_type(self):
        parser = BasicParserWithCast(int)

        result = parser.parse(5)

        assert_that(result).is_equal_to(5)

    def test_should_raise_when_it_is_not_the_correct_type(self):
        parser = BasicParserWithCast(str)

        assert_that(parser.parse).raises(ParserException).when_called_with(['yo'])


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


class TestListParser:
    def test_should_accept_list(self):
        parser = ListParser(BasicParserWithCast(int))

        result = parser.parse([5])

        assert_that(result).is_equal_to([5])

    def test_should_raise_when_parse_other_than_list(self):
        parser = ListParser(BasicParserWithCast(int))

        assert_that(parser.parse).raises(ParserException).when_called_with(5)


class TestSetParser:
    def test_should_accept_set(self):
        parser = SetParser(BasicParserWithCast(int))

        result = parser.parse({5})

        assert_that(result).is_equal_to({5})

    def test_should_accept_list_as_set(self):
        parser = SetParser(BasicParserWithCast(int))

        result = parser.parse([5])

        assert_that(result).is_equal_to({5})

    def test_should_raise_when_parse_other_than_list(self):
        parser = SetParser(BasicParserWithCast(int))

        assert_that(parser.parse).raises(ParserException).when_called_with(5)
