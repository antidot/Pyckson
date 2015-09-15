# Pyckson
A simple python library to serialize python objects to json


## Concepts
pyckson aims to be a json serializer that favors convention over configuration

* just add @pyckson to your classes
* pyckson uses your __init__ signature to discover the structure of an class
* pyckson expects all your parameters to be type annotated
* pyckson expects that your parameters will be assigned to the object with the same name
* pyckson transform parameter names to camelCase and use it as the json `key`
* unfortunately python does not currently allow lists to be typed, so an special decorator is used to type them


## Exemple

```python
from pyckson import pyckson, serialize


@pyckson
class Foo:
    def __init__(self, arg1: str):
        self.arg1 = arg1


@pyckson
@listtype('a_list', int)
class Bar:
    def __init__(self, a_foo: Foo, a_list: list):
        self.a_foo = a_foo
        self.a_list = a_list


bar = Bar(Foo('foo'), [1, 2, 3])
print(serialize(bar))
```

displays

```
{'aFoo': {'arg1': 'foo'}, 'aList': [1, 2, 3]}
```
