import re

from setuptools import setup, find_packages

with open('src/pyckson/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)
    assert version is not None

setup(name='Pyckson',
      version=version,
      description='A minimalist python object mapper',
      long_description='Pyckson is python library that allows you to simply convert python object to and from json',
      url='https://github.com/antidot/Pyckson',
      author='Jean Giard',
      author_email='opensource@antidot.net',
      license='LGPL',
      classifier=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
          'Programming Language :: Python :: 3'
      ],
      keywords='pyckson json',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      install_requires=['arrow']
      )
