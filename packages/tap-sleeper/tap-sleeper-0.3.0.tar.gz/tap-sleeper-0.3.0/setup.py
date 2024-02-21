# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_sleeper', 'tap_sleeper.schemas', 'tap_sleeper.tests']

package_data = \
{'': ['*']}

install_requires = \
['singer-sdk>=0.35.0,<0.36.0']

entry_points = \
{'console_scripts': ['tap-sleeper = tap_sleeper.tap:TapSleeper.cli']}

setup_kwargs = {
    'name': 'tap-sleeper',
    'version': '0.3.0',
    'description': '`tap-sleeper` is a Singer tap for Sleeper, built with the Meltano SDK for Singer Taps.',
    'long_description': '# tap-sleeper ![logo](logo.gif)\n\n\n[![Singer](https://img.shields.io/badge/Singer-Tap-purple.svg)](https://hub.meltano.com/taps/sleeper)\n[![PyPI](https://img.shields.io/pypi/v/tap-sleeper.svg?color=blue)](https://pypi.org/project/tap-sleeper/)\n[![Python versions](https://img.shields.io/pypi/pyversions/tap-sleeper.svg)](https://pypi.org/project/tap-sleeper/)\n[![Super-Linter](https://github.com/collinprather/tap-sleeper/actions/workflows/super-linter.yml/badge.svg)](https://github.com/collinprather/tap-sleeper/actions/workflows/super-linter.yml)\n[![TestPyPI](https://github.com/collinprather/tap-sleeper/actions/workflows/test-pypi.yml/badge.svg)](https://github.com/collinprather/tap-sleeper/actions/workflows/test-pypi.yml)\n[![Test Tap](https://github.com/collinprather/tap-sleeper/actions/workflows/test-tap.yml/badge.svg)](https://github.com/collinprather/tap-sleeper/actions/workflows/test-tap.yml)\n[![CodeQL](https://github.com/collinprather/tap-sleeper/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/collinprather/tap-sleeper/actions/workflows/codeql-analysis.yml)\n\n`tap-sleeper` is a [Singer](https://hub.meltano.com/singer/spec) tap for the [Sleeper](https://sleeper.app/) [api](https://docs.sleeper.app/), built with the [Meltano Tap SDK](https://sdk.meltano.com), which makes it easy to pull the latest news about or status of any NFL players, or granular information about your fantasy football league.\n\n\n## Installation\n\n```bash\npipx install tap-sleeper\n```\n\n## Configuration\n\n### Accepted Config Options\n\n| **Property**                    | **Type** | **Required** | **Description**                                                                |\n|---------------------------------|----------|--------------|--------------------------------------------------------------------------------|\n| sport                           | string   | True         | Professional sport league, ie nfl, nba, etc                                    |\n| league_id                       | string   | False        | Unique identifier for the sleeper league                                       |\n| trending_players_lookback_hours | integer  | False        | Total hours to lookback when requesting the current trending players           |\n| trending_players_limit          | integer  | False        | Total number of players to return when requesting the current trending players |\n\nA full list of supported settings and capabilities for this\ntap is available by running:\n\n```bash\ntap-sleeper --about\n```\n\n## Usage\n\nYou can easily run `tap-sleeper` by itself or in a pipeline using [Meltano](https://meltano.com/).\n\n### Executing the Tap Directly\n\n```bash\ntap-sleeper --version\ntap-sleeper --help\ntap-sleeper --config CONFIG --discover > ./catalog.json\n```\n\n## Developer Resources\n\n### Initialize your Development Environment\n\n```bash\npipx install poetry\npoetry install\n```\n\n### Create and Run Tests\n\nCreate tests within the `tap_sleeper/tests` subfolder and\n  then run:\n\n```bash\npoetry run pytest\n```\n\nYou can also test the `tap-sleeper` CLI interface directly using `poetry run`:\n\n```bash\npoetry run tap-sleeper --help\n```\n\n### Testing with [Meltano](https://www.meltano.com)\n\n_**Note:** This tap will work in any Singer environment and does not require Meltano.\nExamples here are for convenience and to streamline end-to-end orchestration scenarios._\n\nYour project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in\nthe file.\n\nNext, install Meltano (if you haven\'t already) and any needed plugins:\n\n```bash\n# Install meltano\npipx install meltano\n# Initialize meltano within this directory\ncd tap-sleeper\nmeltano install\n```\n\nNow you can test and orchestrate using Meltano:\n\n```bash\n# Test invocation:\nmeltano invoke tap-sleeper --version\n# OR run a test `elt` pipeline:\nmeltano elt tap-sleeper target-jsonl\n```\n\n### SDK Dev Guide\n\nSee the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to\ndevelop your own taps and targets.\n',
    'author': 'Collin Prather',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/collinprather/tap-sleeper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
