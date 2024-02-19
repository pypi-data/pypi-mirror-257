# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avesta', 'avesta.corpus_readers', 'avesta.tools']

package_data = \
{'': ['*']}

install_requires = \
['Levenshtein==0.25.0', 'PersianStemmer==1.0.0', 'tqdm==4.66.2']

setup_kwargs = {
    'name': 'avesta',
    'version': '0.6',
    'description': '',
    'long_description': None,
    'author': 'Majid Fahandezi Sadi',
    'author_email': 'mfsadi.work@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
