# -*- coding: utf-8 -*-
import os
from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    print("Can't import pypandoc - using README.md without converting to RST")
    long_description = open('README.md').read()

with open("LICENSE") as f:
    license = f.read()

with open(".env") as f:
    line = f.readline()
    while line:
        k, v = line.split("\n")[0].split("=")
        os.environ.update({k: v})
        line = f.readline()

setup(
    name='xross_common',
    version='1.1.8',
    description='Common library for alunir',
    long_description=long_description,
    author='jimako1989',
    author_email='alunir@hotmail.com',
    url='https://github.com/alunir/xross_common',
    dependency_links=[],
    license=license,
    install_requires=[
        'logutils==0.3.5',
        'python-dateutil==2.6.0',
        'pykka==2.0.0',
        'oslash==0.5.1',
        'pypandoc==1.4',
        'sphinx'
    ],
    packages=['xross_common'],
    test_suite='tests'
)
