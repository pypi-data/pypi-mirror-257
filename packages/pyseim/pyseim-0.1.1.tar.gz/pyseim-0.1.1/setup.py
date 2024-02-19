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
    'version': '0.1.1',
    'description': 'Waveform viewer and analyzer for ngspice/kicad',
    'long_description': '# PyS(e)im\nPyS(e)im is an open source waveform viewer.\nIt is meant to play together with ngspice and kicad. With just one click you can netlist, simulate and show the simulation results in a window:\n![Example](doc/example.png)\n\nMake sure to include something like the following in your ngspice control section:\n``` spice\n.probe alli\n.control\n\tsave all\n    tran 100n 1m uic\n    run\n    write\n.endc\n```\nWhen running ngspice it should create a `rawspice.raw` file\n\n\n\n# How to use?\n\nPyS(e)im is available on pypi:\n``` bash\npip install pyseim\npyseim --help\n```\n\n# Features\n\n- Netlist, simulate and show results with just one click\n- Equation support\n\n# Alpha Status\n\n- Only tested with Mac\n- Only transient simulations working currently\n- All signals in one plot\n\nIt is a very simple script (currently just one file). However, I find it already quite useful.\n\n# Ideas\n\n- Show SOA violations\n- Support for AC simulations\n- ...\n\n# Contribute\n\nFeel free to contribute.\n\n# Fun Fact\nThe package name is close to PySim that was already taken. PyS(e)im is a close match. Seim means \'viscous juice\'. Therefore, the icon is a honeycomb.\n![Example](pyseim/icon/icon.png)\n\n# Credits\n\nI took some icons from here:\n\n- <a href="https://www.flaticon.com/free-icons/honey" title="honey icons">Honey icons created by imaginationlol - Flaticon</a>\n\n- <a href="https://www.flaticon.com/free-icons/document" title="document icons">Document icons created by bqlqn - Flaticon</a>\n\n- <a href="https://www.flaticon.com/free-icons/refresh" title="refresh icons">Refresh icons created by Dave Gandy - Flaticon</a>\n',
    'author': 'Florian Renneke',
    'author_email': 'florian.renneke@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Renneke/PySeim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
