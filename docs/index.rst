.. Pyckson documentation master file, created by
   sphinx-quickstart on Sat Nov 26 22:31:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. highlight:: python

Welcome to Pyckson's documentation!
===================================

Pyckson is a Python library to transform python objects to and from json.

Pyckson introspects your class __init__ signature to discover it's structure.
::

    class Example:
        def __init__(self, things: List[int]):
            self.things = things

::

    >>> from pyckson import serialize
    >>> serialize(Example([1, 2, 3]))
    {'things': [1, 2, 3]}


User Documentation
==================

.. toctree::
   :maxdepth: 2

   install
   quickstart
   advanced


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

