class ListType:
    def __init__(self, sub_type: type):
        self.sub_type = sub_type

    def __repr__(self):
        return '<class \'list[{}]\'>'.format(self.sub_type.__name__)


class UnresolvedListType:
    def __init__(self, sub_type_provider):
        self.sub_type_provider = sub_type_provider

    @property
    def sub_type(self):
        return self.sub_type_provider()

    def __repr__(self):
        return '<class \'list[{}]\'>'.format(self.sub_type.__name__)


class PycksonAttribute:
    def __init__(self, python_name, json_name, attr_type, optional=False, inline=False):
        self.python_name = python_name
        self.json_name = json_name
        self.attr_type = attr_type
        self.optional = optional
        self.inline = inline

    def __repr__(self):
        return 'PycksonAttribute({}, {}, {}, {}, {})'.format(self.python_name,
                                                             self.json_name,
                                                             self.attr_type,
                                                             self.optional,
                                                             self.inline)


class PycksonUnresolvedAttribute:
    def __init__(self, python_name, json_name, type_provider, optional=False, inline=False):
        self.python_name = python_name
        self.json_name = json_name
        self.type_provider = type_provider
        self.optional = optional
        self.inline = inline

    @property
    def attr_type(self):
        return self.type_provider()

    def __repr__(self):
        return 'PycksonUnresolvedAttribute({}, {}, {}, {}, {})'.format(self.python_name,
                                                                       self.json_name,
                                                                       self.attr_type,
                                                                       self.optional,
                                                                       self.inline)


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
