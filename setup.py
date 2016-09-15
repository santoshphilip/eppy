
import os

import eppy
from setuptools import setup


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def read_md(f):
    try:
        from pypandoc import convert
        try:
            return convert(os.path.join(THIS_DIR, f), 'rst')
        except:
            return "Eppy"
    except ImportError:
        print("warning: pypandoc module not found, could not convert Markdown to RST")
        try:
            with open(os.path.join(THIS_DIR, f), 'r') as f_in:
                return f_in.read()
        except:
            return "Eppy"
    

setup(
    name='eppy',
    version=eppy.__version__,
    url='https://github.com/santoshphilip/eppy',
    license='MIT License',
    author='Santosh Philip',
    author_email='eppy_scripting@yahoo.com',
    description='Scripting language for E+ idf files, and E+ output files',
    long_description=read_md('README.md'),
    packages=['eppy', 'eppy.EPlusInterfaceFunctions', 'eppy.geometry', 'eppy.constructions'],
    include_package_data=True,
    platforms='any',
    install_requires = [
        "munch>=2.0.2",
        "beautifulsoup4>=4.2.1",
        "tinynumpy>=1.2.1",
        "six>=1.10.0",
        "decorator>=4.0.10"
        ],
    classifiers = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        ],
    extras_require={
        ':python_version<="2.7"': [
            'pydot>1.0',
            'pyparsing>=2.1.4'
            ],
        ':python_version>="3.5"': [
            'pydot3k',
            ],
        },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
