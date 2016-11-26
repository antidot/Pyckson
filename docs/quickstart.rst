Quickstart
==========

Writing Compatible Classes
--------------------------

Pyckson will assume that the classes you want to transform are written in a certain way :

 * All class fields must be named parameters in your __init__ method
 * All parameters must be assigned to the object with the same name
 * All parameters must be type annotated
::

    class Example:
        def __init__(self, foo: str, bar: List[int]):
            self.foo = foo
            self.bar = bar


Conventions
-----------

Pyckson will produce and read json where your member names will have been tranformed to camelCase.
::

    class CaseTest:
        def __init__(self, some_parameter: str):
            self.some_parameter = some_parameters

::

    >>> pyckson.serialize(CaseTest('foo'))
    {'someParameter': 'foo'}


Serializing Objects
-------------------

The function :py:func:`pyckson.serialize` takes an object and return a dict-like structure.
::

    >>> from pyckson import serialize
    >>> serialize(Example('foo', [1, 2]))
    {'foo': 'foo', 'bar': [1, 2]}


.. autofunction:: pyckson.serialize

Parsing Objects
---------------

The function :py:func:`pyckson.parse` takes a class and a dictionnary and return an instance of the class.
::

    >>> form pyckson import parse
    >>> example = parse(Example, {'foo': 'thing', 'bar': [1, 2, 3]})
    >>> example
    <__main__.Example object at 0x7fb177d86f28>
    >>> example.foo
    'thing'
    >>> example.bar
    [1, 2, 3]

.. autofunction:: pyckson.parse

Utility Functions
-----------------

Pyckson also includes some convenient wrappers to directly manipulate json strings with the json module.

.. autofunction:: pyckson.dump
.. autofunction:: pyckson.dumps
.. autofunction:: pyckson.load
.. autofunction:: pyckson.loads
