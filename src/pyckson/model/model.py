class PycksonAttribute:
    def __init__(self, python_name: str, json_name: str, attr_type, optional: bool, serializer, parser):
        self.python_name = python_name
        self.json_name = json_name
        self.attr_type = attr_type
        self.optional = optional
        self.serializer = serializer
        self.parser = parser

    def __repr__(self):
        return 'PycksonAttribute({}, {}, {}'.format(self.python_name,
                                                    self.json_name,
                                                    self.attr_type)


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
