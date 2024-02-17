# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etb_pg']

package_data = \
{'': ['*']}

install_requires = \
['psycopg>=3.1.18,<4.0.0']

setup_kwargs = {
    'name': 'etb-pg',
    'version': '0.1.1',
    'description': 'Interface for PostgreSQL databases',
    'long_description': None,
    'author': 'Tate Button',
    'author_email': 'yg3bpwn0or679hau8fxi@duck.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
