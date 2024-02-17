# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['eche']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['networkx']

extras_require = \
{'docs': ['mkdocs>=1.5.3,<2.0.0',
          'mkdocs-material>=9.5.9,<10.0.0',
          'mkdocstrings[python]>=0.24.0,<0.25.0',
          'mkdocs-literate-nav>=0.6.1,<0.7.0',
          'mkdocs-gen-files>=0.5.0,<0.6.0',
          'mkdocs-section-index>=0.3.8,<0.4.0']}

setup_kwargs = {
    'name': 'eche',
    'version': '0.1.0',
    'description': 'Little helper for handling entity clusters',
    'long_description': '<p align="center">\n<img src="https://github.com/dobraczka/eche/raw/main/docs/assets/logo.png" alt="eche logo", width=200/>\n</p>\n\n<p align="center">\n<a href="https://github.com/dobraczka/eche/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/eche/actions/workflows/main.yml/badge.svg?branch=main"></a>\n<a href=\'https://eche.readthedocs.io/en/latest/?badge=latest\'><img src=\'https://readthedocs.org/projects/eche/badge/?version=latest\' alt=\'Documentation Status\' /></a>\n<a href="https://pypi.org/project/eche"/><img alt="Stable python versions" src="https://img.shields.io/pypi/pyversions/eche"></a>\n<a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;"></a>\n</p>\n\nUsage\n=====\nEche provides a `ClusterHelper` class to conveniently handle entity clusters.\n\n```python\n  from eche import ClusterHelper\n  ch = ClusterHelper([{"a1", "b1"}, {"a2", "b2"}])\n  print(ch.clusters)\n  {0: {\'a1\', \'b1\'}, 1: {\'a2\', \'b2\'}}\n```\n\nAdd an element to a cluster\n\n```python\n  ch.add_to_cluster(0, "c1")\n  print(ch.clusters)\n  {0: {\'a1\', \'b1\', \'c1\'}, 1: {\'a2\', \'b2\'}}\n```\n\nAdd a new cluster\n\n```python\n  ch.add({"e2", "f1", "c3"})\n  print(ch.clusters)\n  {0: {\'a1\', \'b1\', \'c1\'}, 1: {\'a2\', \'b2\'}, 2: {\'f1\', \'e2\', \'c3\'}}\n```\n\nRemove an element from a cluster\n\n```python\n  ch.remove("b1")\n  print(ch.clusters)\n  {0: {\'a1\', \'c1\'}, 1: {\'a2\', \'b2\'}, 2: {\'f1\', \'e2\', \'c3\'}}\n```\n\nThe ``__contains__`` function is smartly overloaded. You can check if an entity is in the `ClusterHelper`:\n\n```python\n  "a1" in ch\n  # True\n```\n\nIf a cluster is present\n\n```python\n  {"c1","a1"} in ch\n  # True\n```\n\nAnd even if a link exists or not\n\n```python\n  ("f1","e2") in ch\n  # True\n  ("a1","e2") in ch\n  # False\n```\n\nTo know the cluster id of an entity you can look it up with\n\n```python\n  print(ch.elements["a1"])\n  0\n```\n\nTo get members of a cluster either use\n\n```python\n  print(ch.members(0))\n  {\'a1\', \'b1\', \'c1\'}\n```\n\nor simply\n\n```python\n  print(ch[0])\n  {\'a1\', \'b1\', \'c1\'}\n```\n\nMore functions can be found in the [Documentation](https://eche.readthedocs.io).\n\nInstallation\n============\nSimply use `pip` for installation:\n```\npip install eche\n```\n',
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dobraczka/eche',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
