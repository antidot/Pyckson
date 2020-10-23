from pyckson.const import get_cls_attr, has_cls_attr, PYCKSON_RULE_ATTR, PYCKSON_ENUM_OPTIONS

global_defaults = []


def set_defaults(*args):
    global global_defaults
    for arg in args:
        if not has_cls_attr(arg, PYCKSON_RULE_ATTR):
            raise ValueError('Cannot use {} as a default rule'.format(arg.__name__))
        global_defaults.append(arg)


def reset_defaults():
    global global_defaults
    global_defaults = []


def apply_defaults(cls):
    global global_defaults
    for default in global_defaults:
        default_attr = get_cls_attr(default, PYCKSON_RULE_ATTR)
        if default_attr != PYCKSON_ENUM_OPTIONS and not has_cls_attr(cls, default_attr):
            default(cls)


def apply_enum_default(cls):
    global global_defaults
    for default in global_defaults:
        default_attr = get_cls_attr(default, PYCKSON_RULE_ATTR)
        if default_attr == PYCKSON_ENUM_OPTIONS and not has_cls_attr(cls, default_attr):
            default(cls)
