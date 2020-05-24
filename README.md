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
        'pippin',
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

This will produce (or update) `.pippin` file, which you are supposed to commit into the repo.

```
$ ./setup.py pin [(--tests|--develop)]
```

Pinned dependencies:
--------------------

Installing pinned dependencies:

```
$ ./setup.py sync --pinned [(--tests|--develop)]

```

Additional pip options:
-----------------------

```
$ ./setup.py sync -- <everything-else-will-be-passed-to-pip-install>
