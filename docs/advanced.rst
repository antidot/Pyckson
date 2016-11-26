Advanced Usage
==============

Enums
-----

Pyckson can serialize and parse enums using the :py:meth:`Enum.name` function.

Sometimes it's convenient to parse enums in a case-insensitive way, to do so you can use the :py:func:`pyckson.caseinsensitive` decorator.

.. autofunction:: pyckson.caseinsensitive
