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
import subprocess
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

README_FILE = open('README.md', 'r')


def get_version():
    """
    Get the version from git or from the VERSION file

    If we're in a git repository, uses the output of ``git describe`` as
    the version, and update the ``VERSION`` file.
    Otherwise, read the version from the ``VERSION`` file

    Much inspire from this post:
    http://dcreager.net/2010/02/10/setuptools-git-version-numbers/
    """

    # TODO : READ THE VALUE RETURNED BY GIT DESCRIBE : IF NOT EQUALS 0,
    #        PRINT AN ERROR MESSAGE AND SUGGEST TO LOOK IF ANY TAGS EXISTS.
    #        Afficher un message pour expliciter les erreurs :
    #        - cas où la commande git n'existe pas
    #        - cas où le répertoire courrant n'est pas un référentiel git
    #        - cas où il n'y a pas de tags dans le référentiel git
    def get_version_from_git():
        """Returns the version as defined by ``git describe``, or None."""
        try:
            p = subprocess.Popen(['git', 'describe'],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.stderr.close()
            line = p.stdout.readlines()[0].strip()
            assert line.startswith('v')
            return line[1:] #remove the leading 'v'
        except OSError:
            return None
        except IndexError:
            return None

    def get_version_from_file():
        """Returns the version as defined in the ``VERSION`` file."""
        f = open('VERSION', 'r')
        try:
            version = f.readlines()[0].strip()
        except OSError:
            return None
        finally:
            f.close()
        return version

    def update_version_file(version):
        """Update, if necessary, the ``VERSION`` file."""
        if version != get_version_from_file():
            f = open('VERSION', 'w')
            f.write(version + '\n')
            f.close()

    version = get_version_from_git()
    if version:
        update_version_file(version)
    else:
        version = get_version_from_file()
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
      long_description=README_FILE.read(),
      maintainer='Jeremie DECOCK',
      maintainer_email='jd.jdhp@gmail.com',
      name='pyax12',
      packages=PACKAGES,
      platforms=['Linux'],
      requires=['pyserial'],
      scripts=SCRIPTS.values(),
      url='http://www.jdhp.org/',
      version=get_version())

README_FILE.close()
