import sys

collect_ignore = []
if sys.version_info < (3, 7):
    collect_ignore.append('test_inheritance.py')
    collect_ignore.append('test_dataclass.py')

if sys.version_info < (3, 11):
    collect_ignore.append('test_list_typing.py')
