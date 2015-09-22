class ListType:
    def __init__(self, sub_type: type):
        self.sub_type = sub_type

    def __repr__(self):
        return '<class \'list[{}]\'>'.format(self.sub_type.__name__)


class PycksonAttribute:
    def __init__(self, python_name, json_name, attr_type, optional=False):
        self.python_name = python_name
        self.json_name = json_name
        self.attr_type = attr_type
        self.optional = optional

    def __repr__(self):
        return 'PycksonAttribute({}, {}, {}, {})'.format(self.python_name,
                                                         self.json_name,
                                                         self.attr_type,
                                                         self.optional)


class PycksonModel:
    def __init__(self, attributes):
        self.attributes = attributes

    def get_attribute(self, python_name) -> PycksonAttribute:
        for attr in self.attributes:
            if attr.python_name == python_name:
                return attr
        raise KeyError('no attribute {} found'.format(python_name))

    def __repr__(self):
        return repr(self.attributes)
