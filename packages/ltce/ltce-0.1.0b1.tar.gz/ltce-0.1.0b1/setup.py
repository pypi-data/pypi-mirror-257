#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

description = 'This module is for estimating long-term causal effect. Please follow the guide of each method.'
try:
    with open("README.rst", "r") as f:
        long_description = f.read()
except Exception as e:
    long_description = description
REQUIRES_PYTHON = '>=3.6.0'
REQUIREMENT = [
    'matplotlib', 'pandas', 'numpy' 
]

setup(
    name='ltce',
    version='0.1.0b1',
    description=description,
    long_description=long_description,
    author='yuanyuzhang',
    author_email='zhangyuanyu2015@gmail.com',
    maintainer='yuanyuzhang',
    maintainer_email='zhangyuanyu2015@gmail.com',
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIREMENT,
    platforms=["all"],
    url='https://github.com/zhangyuanyuzyy/LT-Transformer',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)