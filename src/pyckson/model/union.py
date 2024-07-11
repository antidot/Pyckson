from typing import Tuple, Union


def inspect_optional_typing(annotation) -> Tuple[bool, type]:
    # seems like at some point internal behavior on typing Union changed
    # https://bugs.launchpad.net/ubuntu/+source/python3.5/+bug/1650202
    if "Union" not in str(annotation) and "Optional" not in str(annotation):
        return False, type(None)

    if hasattr(annotation, '__origin__'):
        is_union = annotation.__origin__ == Union
    else:
        is_union = issubclass(annotation, Union)

    if not is_union:
        return False, type(None)

    if hasattr(annotation, '__args__'):
        union_params = annotation.__args__
    else:
        union_params = annotation.__union_params__

    try:
        is_optional = isinstance(None, union_params[-1])
    except TypeError:
        is_optional = False
    if is_optional:
        union_param = Union[union_params[:-1]]
    elif len(union_params) > 1:
        union_param = Union[union_params]
    else:
        union_param = union_params[0]
    return is_optional, union_param
