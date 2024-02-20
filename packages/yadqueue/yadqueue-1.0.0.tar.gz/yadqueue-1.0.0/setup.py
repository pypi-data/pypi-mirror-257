
from io import open
from setuptools import setup

"""
:authors: sesh00
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2024 sesh00
"""

version = '1.0.0'



setup(
    name='yadqueue',
    version=version,

    author='sesh00',
    author_email='ernestrsage@gmail.com',

    description=(
        u'Python library for interacting with a queue service API'
    ),
    #long_description=long_description,
    #long_description_content_type='text/markdown',

    url='https://github.com/sesh00/yadqueue',
    download_url='https://github.com/sesh00/yadqueue/archive/main.zip'.format(
        version
    ),

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['yadqueue'],
    install_requires=['requests'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)