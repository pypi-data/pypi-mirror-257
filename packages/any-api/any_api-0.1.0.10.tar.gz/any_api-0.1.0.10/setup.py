# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['any_api',
 'any_api.asyncapi',
 'any_api.asyncapi.model',
 'any_api.base_api',
 'any_api.base_api.model',
 'any_api.openapi',
 'any_api.openapi.model',
 'any_api.openapi.model.openapi',
 'any_api.openapi.to',
 'any_api.openapi.web_ui',
 'any_api.util']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.2,<3.0.0,!=2.0.3,!=2.1.0']

setup_kwargs = {
    'name': 'any-api',
    'version': '0.1.0.10',
    'description': 'Quick and easy to create OpenAPI/AsyncAPI, and provide corresponding extensions',
    'long_description': 'None',
    'author': 'so1n',
    'author_email': 'qaz6803609@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
