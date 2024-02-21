# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode', 'majormode.perseus', 'majormode.perseus.utils']

package_data = \
{'': ['*']}

install_requires = \
['perseus-core-library>=1.19,<2.0', 'python-dotenv>=1.0,<2.0']

setup_kwargs = {
    'name': 'perseus-getenv-library',
    'version': '1.0.5',
    'description': 'Python library helper for reading environment variables',
    'long_description': '# Perseus GetEnv Python Library\n\nMajormode Perseus GetEnv Python Library is a helper library to read environment variables.\n\nThis library relies on [`python-dotenv`](https://github.com/theskumar/python-dotenv) to read key-value pairs from a `.env` file, which helps in the development of applications following the [12-factor principles](https://12factor.net/).\n\nThis library provides a helper function to convert the value of environment variables in the expected data type.\n\n## Installation\n\nTo install [Perseus GetEnv Python Library](https://github.com/dcaune/perseus-getenv-python-library), simply enter the follow command line:\n\n``` shell\npip install perseus-getenv-library\n```\n',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/majormode/perseus-getenv-python-library',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
