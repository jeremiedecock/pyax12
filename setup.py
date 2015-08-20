#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PyAX-12

# The MIT License
#
# Copyright (c) 2010,2015 Jeremie DECOCK (http://www.jdhp.org)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from distutils.core import setup
import os
import shutil

# See :  http://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = ['Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Operating System :: POSIX :: Linux',
               'Programming Language :: Python :: 3.0',
               'Topic :: System :: Hardware :: Hardware Drivers']

PACKAGES = ['pyax12']

README_FILE = 'README.rst'

def get_long_description():
    with open(README_FILE, 'r') as fd:
        desc = fd.read()
    return desc

def get_version():
    version = __import__('pyax12').__version__
    return version


# Prepare scripts ###########

# The list of scripts we want to export in the distrib ({'src': 'dest', ...}).
SCRIPTS = {}

for source, dest in SCRIPTS.iteritems():
    try:
        os.mkdir(os.path.dirname(dest))
    except OSError:
        pass # TODO

    try:
        shutil.copyfile(source, dest)
    except IOError:
        pass # TODO


# Don't use unicode strings in setup arguments or bdist_rpm will fail.
setup(author='Jeremie DECOCK',
      author_email='jd.jdhp@gmail.com',
      classifiers=CLASSIFIERS,
      description='A library to control dynamixel AX-12+ servos with python',
      license='MIT license',
      long_description=get_long_description(),
      maintainer='Jeremie DECOCK',
      maintainer_email='jd.jdhp@gmail.com',
      name='pyax12',
      packages=PACKAGES,
      platforms=['Linux'],
      requires=['pyserial'],
      scripts=SCRIPTS.values(),
      url='http://www.jdhp.org/',
      version=get_version())
