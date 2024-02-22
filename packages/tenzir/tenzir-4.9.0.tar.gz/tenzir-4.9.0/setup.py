# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tenzir', 'tenzir.tenzir', 'tenzir.tools', 'tenzir.utils']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.2,<4.0', 'pyarrow>=11,<16']

extras_require = \
{'module': ['numpy>=1.24,<2.0'],
 'operator': ['python-box>=7.0,<8.0', 'pandas>=2.1.3,<3.0.0']}

setup_kwargs = {
    'name': 'tenzir',
    'version': '4.9.0',
    'description': 'A security telemetry engine for detection and response',
    'long_description': '# Tenzir Python\n\nThe Python package of Tenzir provides a flexible control plane to integrate Tenzir\nwith other security tools.\n\n> **Note**\n> The Python effort is still highly experimental and subject to rapid change.\n> Please do not consider it for production use.\n\n## Usage\n\nTo get started, clone the Tenzir repository and install the Python package via\n[Poetry](https://python-poetry.org/docs/):\n\n```bash\ngit clone https://github.com/tenzir/tenzir.git\ncd tenzir/python\npoetry install -E module\n```\n\n## Development\n\nWe recommend that you work with an editable installation, which is the default\nfor `poetry install`.\n\n### Unit Tests\n\nRun the unit tests via pytest:\n\n```bash\npoetry run pytest\n```\n\n### Integration Tests\n\nRun the integrations tests via Docker Compose and pytest:\n\n```bash\n./docker-poetry-run.sh pytest -v\n```\n\n## Packaging\n\nThe following instructions concern maintainers who want to publish the Python\npackage to PyPI.\n\n> **Note**\n> Our releasing scripts and CI run these steps automatically. You do not need to\n> intervene anywhere. The instructions below merely document the steps taken.\n\n### Bump the version\n\nPrior to releasing a new version, bump the version, e.g.:\n\n```bash\npoetry version 2.3.1\n```\n\nThis updates the `pyproject.toml` file.\n\n### Publish to Test PyPI\n\n1. Add a Test PyPi repository:\n\n   ```bash\n   poetry config repositories.test-pypi https://test.pypi.org/legacy/\n   ```\n\n2. Get the token from <https://test.pypi.org/manage/account/token/>.\n\n3. Store the token:\n\n  ```bash\n  poetry config pypi-token.test-pypi pypi-XXXXXXXX\n  ```\n\n4. Publish:\n  \n   ```bash\n   poetry publish --build -r test-pypi\n   ```\n\n### Publish to PyPI\n\n1. Get the token from <https://pypi.org/manage/account/token/>.\n\n2. Store the token:\n\n  ```bash\n  poetry config pypi-token.pypi pypi-XXXXXXXX\n  ```\n\n3. Publish\n\n   ```bash\n   poetry publish --build\n   ```\n',
    'author': 'Tenzir',
    'author_email': 'engineering@tenzir.com',
    'maintainer': 'Tenzir',
    'maintainer_email': 'engineering@tenzir.com',
    'url': 'https://tenzir.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
