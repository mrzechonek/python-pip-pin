import logging
import os.path
import subprocess
import sys
import tempfile

import pip_pin
import pytest


@pytest.fixture(scope="session")
def virtualenv():
    with tempfile.TemporaryDirectory() as tmpdir:
        venv = os.path.join(tmpdir, "venv")
        logging.info("Create virtualenv in %s", venv)
        subprocess.check_call([sys.executable, "-m", "venv", venv], stdout=None)
        python = os.path.join(venv, "bin", "python")
        logging.info("Install pippin in %s", venv)
        subprocess.check_call(
            [
                python,
                "-m",
                "pip",
                "-q",
                "install",
                os.path.dirname(pippin.__path__[0]),
            ]
        )
        yield python


@pytest.fixture
def pypi():
    pass


@pytest.fixture(autouse=True)
def pypi_mock(pypi):
    pass


@pytest.fixture
def package_dependencies():
    return dict(install_requires=[], tests_require=[], develop_requires=[],)


@pytest.fixture
def package(package_dependencies, tmpdir):
    pass
