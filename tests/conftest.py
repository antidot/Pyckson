import sys

if sys.version_info < (3, 7):
    collect_ignore = ['test_inheritance.py', 'test_dataclass.py']
