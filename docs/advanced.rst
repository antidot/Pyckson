Advanced Usage
==============

Enums
-----

Pyckson can serialize and parse enums using the :py:meth:`Enum.name` function.

Sometimes it's convenient to parse enums in a case-insensitive way, to do so you can use the :py:func:`pyckson.caseinsensitive` decorator.

.. autofunction:: pyckson.caseinsensitive

Dates
-----

By default Pyckson does not apply any special treatment to date objects, meaning that if you use serialize you will get a dictionnary with date-type values, and json.dumps will not be able to serialize your object.

You can override this behavior globally or on a specific class to fit your needs.

The function :py:func:`pyckson.configure_date_formatter` will set an application-wide behavior, and you can use the :py:func:`pyckson.date_formatter` decorator to override serialization behavior for fields of a class (it does not apply recursively).

Custom Date Formatters
----------------------

Pyckson provides two date formatters based on the arrow library : :py:class:`pyckson.date.arrow.ArrowStringFormatter` and :py:class:`pyckson.date.arrow.ArrowTimestampFormatter`.

To use them configure them appropriately like
::

    import pyckson
    from pyckson.date.arrow import ArrowStringFormatter
    pyckson.configure_date_formatter(ArrowStringFormatter())

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
    pyckson.configure_explicit_nulls(use_explicit_nulls=True)

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

