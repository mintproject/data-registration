#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()

def find_package_data(dirname):
    def find_paths(dirname):
        items = []
        for fname in os.listdir(dirname):
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                items += find_paths(path)
            elif not path.endswith(".py") and not path.endswith(".pyc"):
                items.append(path)
        return items

    items = find_paths(dirname)
    return [os.path.relpath(path, dirname) for path in items]



setup(
    name='data_registration',
    version='0.1.0',
    author='Maximiliano Osorio',
    author_email='mosorio@isi.edu',
    maintainer='Maximiliano Osorio',
    maintainer_email='mosorio@isi.edu',
    license='MIT',
    url='https://github.com/mintproject/data_registration',
    description='Python to upload data to the MINT DataCatalog',
    long_description=read('README.md'),
    python_requires='>=3.5',
    install_requires=[
        'scipy',
        'requests',
        'xarray'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={"data_registration": find_package_data("src/data_registration")},
    zip_safe=False,
)

