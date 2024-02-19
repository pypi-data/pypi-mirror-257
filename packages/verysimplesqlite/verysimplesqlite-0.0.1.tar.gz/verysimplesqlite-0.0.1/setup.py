# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['verysimplesqlite']
setup_kwargs = {
    'name': 'verysimplesqlite',
    'version': '0.0.1',
    'description': '1000-7 calculyator',
    'long_description': '',
    'author': 'fikko',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
