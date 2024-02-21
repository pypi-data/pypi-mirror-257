# puts - Python Utility Tools

Python high-level helper classes and functions.

[![](https://img.shields.io/pypi/v/puts)](https://pypi.org/project/puts/)
[![](https://img.shields.io/pypi/dm/puts)](https://pypistats.org/packages/puts)
[![](https://img.shields.io/badge/license-MIT-blue)](https://github.com/MarkHershey/puts/blob/master/LICENSE)
[![](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

## Install

-   Prerequisite: Python 3.6+

```bash
pip install --upgrade puts
```

## Usage

### Logging with Colored Output

```python
from puts import get_logger

logger = get_logger()

logger.debug("Hello world!")
logger.info("Hello world!")
logger.warning("Hello world!")
logger.error("Hello world!")
logger.critical("Hello world!")
```

## Development

### Set up dev environment

-   _clone this repo_
    ```bash
    $ git clone https://github.com/MarkHershey/puts.git
    ```
-   _go to project root_
    ```bash
    $ cd puts
    ```
-   _create virtual env for this project_
    ```bash
    $ python -m venv venv
    $ source venv/bin/activate
    $ pip install --upgrade pip wheel setuptools
    ```
-   _install this package in **editable** mode_
    ```bash
    $ pip install -e ".[dev]"
    ```

### Run tests

```bash
$ pytest
```

## Disclaimer

-   This package is highly opinionated, it does not intend to cater to every use case.
-   It is only intended for personal projects usage (for now).
