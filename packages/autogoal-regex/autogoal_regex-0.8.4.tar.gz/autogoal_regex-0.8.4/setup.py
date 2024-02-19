# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autogoal_regex']

package_data = \
{'': ['*']}

install_requires = \
['autogoal-contrib>=0.8.2,<0.9.0', 'autogoal>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'autogoal-regex',
    'version': '0.8.4',
    'description': 'scikit-learn algorithm library for AutoGOAL',
    'long_description': '# AutoGOAL REGEX Algorithm Library',
    'author': 'Suilan Estevez-Velarde',
    'author_email': 'suilanestevez@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://autogoal.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.13,<3.11',
}


setup(**setup_kwargs)
