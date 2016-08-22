from setuptools import setup, find_packages

setup(name='Pyckson',
      version='0.4.2',
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
      packages=find_packages(exclude=['pyckson.test']),
      install_requires=[],
      test_suite='pyckson.test')
