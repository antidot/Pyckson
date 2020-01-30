# Pyckson
A simple python library to serialize python objects to json

[![Build Status](https://travis-ci.org/antidot/Pyckson.svg?branch=master)](https://travis-ci.org/antidot/Pyckson)
[![Documentation Status](http://readthedocs.org/projects/pyckson/badge/?version=latest)](http://pyckson.readthedocs.io/en/latest/?badge=latest)

## Concepts
pyckson aims to be a json serializer/parser that favors convention over configuration

* pyckson uses your __init__ signature to discover the structure of a class
* pyckson expects all your parameters to be type annotated
* pyckson expects that your parameters will be assigned to an attribute with the same name
* pyckson transform parameter names to camelCase and use it as the json `key`


## Example

```python
from pyckson import pyckson, listtype, serialize, parse

class Foo:
    def __init__(self, arg1: str):
        self.arg1 = arg1
    
    def __str__(self):
        return 'Foo({})'.format(self.arg1)

class Bar:
    def __init__(self, a_foo: Foo, a_list: List[int]):
        self.a_foo = a_foo
        self.a_list = a_list
        
    def __str__(self):
        return 'Bar({}, {})'.format(self.a_foo, self.a_list)
```


```python
bar = Bar(Foo('foo'), [1, 2, 3])
print(serialize(bar))
```

displays

```
{'aFoo': {'arg1': 'foo'}, 'aList': [1, 2, 3]}
```

```python
bar = parse(Bar, {'aFoo': {'arg1': 'foo'}, 'aList': [1, 2, 3]})
print(str(bar))
```

displays

```
Bar(Foo(foo), [1, 2, 3])
```

## Documentation

Documentation is available at <http://pyckson.readthedocs.io/en/latest/>

## Contact

opensource@antidot.net

## Why pyckson

I Wanted a non-intrusive library to serialize my classes.
I also want my classes to be as close to native python as possible (for IDE completion for example).

Cons : pyckson is not very flexible in serialization options, do not use it if you need to parse exeternal formats with lots of corner cases.

## Noteworthy

Pyckson serialize to dict-like structures, so you can use to serialize to mongo bson format and use native datetime and bytes fields.
