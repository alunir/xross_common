# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    print("Can't import pypandoc - using README.md without converting to RST")
    long_description = open('README.md').read()

with open("LICENSE") as f:
    license = f.read()

os.environ.update({"CONFIG_DIR": "tests"})

setup(
    name='xross_common',
    version='1.0',
    description='Common library for alunir',
    long_description=long_description,
    author='jimako1989',
    author_email='alunir@hotmail.com',
    url='https://github.com/alunir/xross_common',
    dependency_links=[],
    license=license,
    install_requires=[
        'logutils==0.3.5',
        'multiprocessing_logging==0.2.5',
        'python-dateutil==2.6.0',
        'munch==2.1.1',
        'pypandoc==1.4',
        'sphinx'
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests'
)
