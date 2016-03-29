
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import eppy

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.txt')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='eppy',
    version=eppy.__version__,
    url='https://github.com/santoshphilip/eppy',
    license='MIT License',
    author='Santosh Philip',
    tests_require=['pytest'],
    install_requires=["munch>=2.0.2",
                "beautifulsoup4>=4.2.1",
                # "numpy>=1.7.1",
                "pyparsing>=pyparsing",
                "pydot>1.0",
                "pytest>=2.3.5",
                    ],
    cmdclass={'test': PyTest},
    author_email='eppy_scripting@yahoo.com',
    description='Scripting language for E+ idf files, and E+ output files',
    long_description=long_description,# TODO set this up
    packages=['eppy', 'eppy.EPlusInterfaceFunctions', 'eppy.geometry'],
    include_package_data=True,
    platforms='any',
    test_suite='eppy.test.test_eppy',# TODO make test_eppy
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
