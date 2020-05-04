Advanced Usage
==============

Defaults
--------

If you want to apply a specific pyckson behavior without having to annotate all your classes, you can configure a global decorator using :py:func:`pyckson.set_defautls`.

Most class level decorators are viable candidates. You can pass multiple arguments, or call the function multiple time to accumulate behaviors.

::

    from pyckson import set_default, no_camel_case, date_formatter
    from pyckson.date.arrow import ArrowStringFormatter
    set_defaults(no_camel_case, date_formatter(ArrowStringFormatter()))


Enums
-----

Pyckson can serialize and parse enums using the :py:meth:`Enum.name` function.

Sometimes it's convenient to parse enums in a case-insensitive way, to do so you can use the :py:func:`pyckson.caseinsensitive` decorator.

.. autofunction:: pyckson.caseinsensitive

Dates
-----

By default Pyckson does not apply any special treatment to date objects, meaning that if you use serialize you will get a dictionnary with date-type values, and json.dumps will not be able to serialize your object.

You can use the :py:func:`pyckson.date_formatter` decorator to override serialization behavior for fields of a class (it does not apply recursively), or configure it globally with :py:func:`pyckson.set_defautls`.

Custom Date Formatters
----------------------

Pyckson provides two date formatters based on the arrow library : :py:class:`pyckson.date.arrow.ArrowStringFormatter` and :py:class:`pyckson.date.arrow.ArrowTimestampFormatter`.

To use them configure them appropriately like
::

    import pyckson
    from pyckson.date.arrow import ArrowStringFormatter
    pyckson.set_defaults(pyckson.date_formatter(ArrowStringFormatter()))

or

::

    import pyckson
    from pyckson.date.arrow import ArrowStringFormatter

    @pyckson.date_formatter(ArrowStringFormatter())
    class Foo:
        def __init__(bar: datetime):
            self.bar = bar

You should then be able to properly serialize dates to json-strings

::

    >>> pyckson.dumps(Foo(datetime(2018, 3, 8, 13, 58, 0)))
    '{"bar": "2013-05-05T13:58:00+00:00"}'


Nulls serialisation
-------------------

By default pyckson will not serialize optional empty attributes.
You can switch this behavior and force it to assign the null value to the generated json.

::

    import pyckson
    pyckson.set_defaults(pyckson.explicit_nulls)

or

::

    import pyckson

    @pyckson.explicit_nulls()
    class Foo:
        def __init__(bar: Optional[str] = None):
            self.bar = bar

You should see explicit null values in the output

::

    >>> pyckson.dumps(Foo(bar=None))
    '{"bar": null}'

