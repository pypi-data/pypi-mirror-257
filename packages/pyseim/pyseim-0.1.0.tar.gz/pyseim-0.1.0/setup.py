# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyseim']

package_data = \
{'': ['*'], 'pyseim': ['icon/*']}

install_requires = \
['ltspice', 'pyqt5']

entry_points = \
{'console_scripts': ['pyseim = pyseim.main:main']}

setup_kwargs = {
    'name': 'pyseim',
    'version': '0.1.0',
    'description': 'Waveform viewer and analyzer for ngspice/kicad',
    'long_description': 'None',
    'author': 'Florian Renneke',
    'author_email': 'florian.renneke@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
