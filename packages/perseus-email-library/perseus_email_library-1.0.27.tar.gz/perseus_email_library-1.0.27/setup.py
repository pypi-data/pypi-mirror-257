# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode',
 'majormode.perseus',
 'majormode.perseus.constant',
 'majormode.perseus.email',
 'majormode.perseus.email.provider',
 'majormode.perseus.model']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=3.1,<4.0',
 'mailjet-rest>=1.3,<2.0',
 'perseus-core-library>=1.18,<2.0']

setup_kwargs = {
    'name': 'perseus-email-library',
    'version': '1.0.27',
    'description': 'Perseus Email Python Library',
    'long_description': '# Perseus: Email Python Library\n\nPerseus Email Python Library is a repository of reusable Python components to compose and send email.\n\nThese components have minimal dependencies on other libraries, so that they can be deployed easily.  In addition, these components will keep their interfaces as stable as possible, so that other Python projects can integrate these components without having to worry about changes in the future.\n\n\nTo install the Perseus Email Python Library, enter the follow command line:\n\n```bash\n$ poetry add perseus-email-library\n```\n',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/majormode/perseus-email-python-library',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
