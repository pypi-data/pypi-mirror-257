# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lovelaice']

package_data = \
{'': ['*']}

install_requires = \
['mistralai>=0.0.12,<0.0.13', 'python-dotenv>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'lovelaice',
    'version': '0.1.0',
    'description': 'An AI-powered chatbot for the terminal and editor',
    'long_description': None,
    'author': 'Alejandro Piad-Morffis',
    'author_email': 'apiad@apiad.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
