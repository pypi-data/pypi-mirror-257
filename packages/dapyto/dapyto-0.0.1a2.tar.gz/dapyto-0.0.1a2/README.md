## Daniel's Python Tools

[![CI](https://github.com/daniel-volk/daniels_python_tools/actions/workflows/ci.yml/badge.svg?event=push)](https://github.com/daniel-volk/daniels_python_tools/actions/workflows/ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

### Stack
* Debian Bookworm (v12.LATEST) -> lsb_release -a
* Python v3.12.LATEST -> python --version

#### Hints
* ...

### Deployment
* Build and check package, using `make build`
* Deploy package to
    * TestPyPI, using `make deploy_test`
    * PyPI, using `make deploy_live`

#### Hints
* Build uses `pyproject.toml` descriptor file
* Deployment to TestPyPI package repository uses `TEST_PYPI_TOKEN` secret
* Deployment to PyPI package repository uses `LIVE_PYPI_TOKEN` secret

### Installation
* From sources (editable), using `make install_local`
* From TestPyPI, using `make install_test`
* From PyPI, using `make install_live`