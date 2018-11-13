#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2018 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The setup script."""
import codecs
import os
import re

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pandas>=0.21.0,<1.0.0',
    'jupyter>=1.0.0,<2.0.0',
    'Pillow>=4.3.0',
    # Avoid selenium bug:
    # https://github.com/SeleniumHQ/selenium/issues/5296
    'selenium>=3.7.0,<=3.8.0',
    'bokeh>=0.12.16,<2.0.0',
    'scipy>=1.0.0,<2.0.0',
    'colour>=0.1.5,<1.0.0'
]

setup_requirements = [

]

test_requirements = [

]

PACKAGE_NAME = 'chartify'

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    """
    Build an absolute path from ``*filenames``, and  return contents of
    resulting file.  Defaults to UTF-8 encoding.
    """
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for fl in filenames:
        with codecs.open(os.path.join(HERE, fl), 'rb', encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


META_FILE = read(os.path.join(PACKAGE_NAME, '__init__.py'))


def find_meta(meta):
    """Extract __*meta*__ from META_FILE."""
    re_str = r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta)
    meta_match = re.search(re_str, META_FILE, re.M)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string.'.format(meta=meta))


setup(
    name=PACKAGE_NAME,
    version=find_meta('version'),
    description="Python library to make plotting simpler for data scientists",
    long_description=readme + '\n\n' + history,
    author=find_meta('author'),
    author_email=find_meta('email'),
    url='https://github.com/spotify/chartify',
    packages=find_packages(include=['chartify']),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='chartify',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    python_requires='>=3.5,<4')
