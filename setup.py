#!/usr/bin/env python
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


VERSION = '0.0.1a1'

long_description = '''bayex implements bayesian networks over
finitely-supported distributions and provides tools for Mendelian
traits modelling in (possibly consanguineous) families.'''


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def exclude_package(pkg):
    for exclude in excluded:
        if pkg.startswith(exclude):
            return True
    return False

def create_package_list(base_package):
    return ([base_package] +
            [base_package + '.' + pkg
             for pkg
             in find_packages(base_package)
             if not exclude_package(pkg)])


setup_info = dict(
    # Metadata
    name='bayex',
    version=VERSION,
    author='Ilya Kolpakov',
    author_email='ilya.kolpakov@gmail.com',
    #url='http://.readthedocs.org/en/latest/',
    #download_url='http://pypi.python.org/pypi/',
    description='Bayesian networks for finitely-supported distributions',
    long_description=long_description,
    license='GPLv2',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Science/Research',
	'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
	'Topic :: Scientific/Engineering :: Statistics',
	'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],

    # Package info
    packages=create_package_list('bayex'),

    # Requirements
    install_requires = ['networkx'],

    # Use pytest
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},

    zip_safe=True,
)


setup(**setup_info)


