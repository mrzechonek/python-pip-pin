THIS IS AN EXPERIMENT. PLAY WITH IT, THINK ABOUT IT, DON'T USE IT ON PRODUCTION.

Let me know what you think.

[![PyPI version shields.io](https://img.shields.io/pypi/v/pip-pin.svg)](https://pypi.python.org/pypi/pip-pin/)

[![PyPI status](https://img.shields.io/pypi/status/pip-pin.svg)](https://pypi.python.org/pypi/pip-pin/)

pip pin
=======

Specify and pin dependencies from `setup.py`.

TL;DR;

```python
from setuptools import find_packages, setup

setup(
    name='meriadok',
    version='1.0.',
    packages=find_packages(),
    setup_requires=[
        'pip-pin',
    ],
    install_requires=[
        'flask',
    ],
    tests_require=[
        'pytest',
    ],
    develop_requires=[
        'black',
    ],
)
```

Non-pinned dependencies:
------------------------

Runtime:
```
$ ./setup.py sync --install
```

Tests:
```
$ ./setup.py sync --tests
```

Development:
```
$ ./setup.py sync --develop
```

Pinning
-------

This will produce (or update) `.pip-pin` directory, which you are supposed to commit into the repo.

```
$ ./setup.py pin [(--install|--tests|--develop)]
```

Pinned dependencies:
--------------------

Installing pinned dependencies:

```
$ ./setup.py sync --pinned [(--install|--tests|--develop)]

```
