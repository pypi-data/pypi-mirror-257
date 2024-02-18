# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spatial3d', 'spatial3d.euler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spatial3d',
    'version': '0.8.0',
    'description': 'A Python library for representing and working with 3D objects.',
    'long_description': '# spatial3d v0.8.0 ![Badge](https://github.com/jbschwartz/spatial/actions/workflows/ci.yml/badge.svg)\n\nA Python library for representing and working with 3D objects.\n\n## Installation\n\nInstall using `pip`:\n\n```\npython -m pip install spatial3d\n```\n\nInstall using `poetry`:\n\n```\npoetry add spatial3d\n```\n',
    'author': 'James Schwartz',
    'author_email': 'james@schwartz.engineer',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jbschwartz/spatial3d',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
