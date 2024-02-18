# SPDX-License-Identifier: MIT


# Import both local and third-party setup modules.
import codecs
import os

from setuptools import find_packages, setup

# Import local modules to fetch version number.
from avro import __version__

# Constants.
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = '\n' + fh.read()


# Call the setup function.
setup(
    name='avro.py',
    version=__version__,
    description='A modern Pythonic implementation of Avro Phonetic.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='HitBlast',
    author_email='hitblastlive@gmail.com',
    url='https://github.com/hitblast/avro.py',
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    package_data={'avro': ['*.md']},
    include_package_data=True,
    license='MIT',
    python_requires='>=3.8',
    keywords=[
        'python',
        'avro',
        'avro phonetic',
        'bangla',
        'bangla phonetics',
        'bengali',
        'bengali phonetics',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
