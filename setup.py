#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

# quick hack, will probably do something better later.
requirements = [
        "configobj",
        "byteplay==0.2",
        "ducktypes>0.2.0, <0.3.0dev"
        ]
if sys.version_info[1] < 7:
    requirements.append("importlib")

setup(name='pydenji',
      description='Dependency Injection Toolkit',
      version='0.6.0.dev0',
      install_requires=requirements,
      long_description=open("README").read(),
      author='Alan Franzoni',
      license='Apache-2.0',
      keywords='dependency injection inversion control ioc container',
      author_email='username@franzoni.eu',
      url='https://github.com/alanfranz/pydenji',
      packages=find_packages(),
      entry_points={
        "console_scripts": [
            "unit=unittest.__main__:main"
        ]
    }
     )
