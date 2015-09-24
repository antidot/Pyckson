# Pyckson
A simple python library to serialize python objects to json

[![Build Status](https://travis-ci.org/antidot/Pyckson.svg?branch=master)](https://travis-ci.org/antidot/Pyckson)

## Concepts
pyckson aims to be a json serializer/parser that favors convention over configuration

* just add @pyckson to your classes
* pyckson uses your __init__ signature to discover the structure of a class
* pyckson expects all your parameters to be type annotated
* pyckson expects that your parameters will be assigned to the object with the same name
* pyckson transform parameter names to camelCase and use it as the json `key`
* unfortunately python (3.4) does not allow lists to be typed, so a special decorator is used to type them


## Example

```python
from pyckson import pyckson, listtype, serialize, parse

@pyckson
class Foo:
    def __init__(self, arg1: str):
        self.arg1 = arg1
    
    def __str__(self):
        return 'Foo({})'.format(self.arg1)

@pyckson
@listtype('a_list', int)
class Bar:
    def __init__(self, a_foo: Foo, a_list: list):
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

## Contact

opensource@antidot.net
