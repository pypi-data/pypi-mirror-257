# -*- coding: utf-8 -*-
# @Time     : 2024/2/20 16:38
# @Author   : Long-Long Qiu
# @FileName : setup.py
# @Product  : PyCharm
# import packages
from __future__ import print_function
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="function_tool",
    version='0.0.4',
    author="DerrickChiu",
    author_email="chiull@foxmail.com",
    description="some usual tool with class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://gitee.com/DerrickChiu/function_tool.git",
    packages=find_packages(),
    install_requires=[

        ],
    classifiers=[
        "Topic :: Scientific/Engineering",
        'Topic :: Scientific/Engineering :: GIS',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)