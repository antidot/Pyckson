from inspect import Parameter, Signature

from pyckson.model import ListType, PycksonAttribute, PycksonModel

from pyckson.helpers import camel_case_name


def build_pyckson_attribute(parameter: Parameter, sub_type: type=None) -> PycksonAttribute:
    json_name = camel_case_name(parameter.name)
    optional = parameter.default is None
    if parameter.annotation is Parameter.empty:
        raise TypeError('parameter {} has no type'.format(parameter.name))
    if parameter.kind != Parameter.POSITIONAL_OR_KEYWORD:
        raise TypeError('pyckson only handle named parameters')
    if parameter.annotation is list:
        if sub_type is None:
            raise TypeError('list parameter {} has no subType'.format(parameter.name))
        return PycksonAttribute(parameter.name, json_name, ListType(sub_type), optional)
    return PycksonAttribute(parameter.name, json_name, parameter.annotation, optional)


def build_pyckson_model(method_signature: Signature, type_info) -> PycksonModel:
    attributes = []
    for name, parameter in method_signature.parameters.items():
        if name == 'self':
            continue
        if name in type_info:
            attribute = build_pyckson_attribute(parameter, type_info[name])
        else:
            attribute = build_pyckson_attribute(parameter)
        attributes.append(attribute)
    return PycksonModel(attributes)
