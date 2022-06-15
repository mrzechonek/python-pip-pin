#!env python

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

# fmt: off
setup(
    name='pip-pin',
    version='0.0.10',
    packages=find_packages(),
    url='https://github.com/mrzechonek/python-pip-pin',
    license='MIT',
    author='Michał Lowas-Rzechonek',
    author_email='michal@rzechonek.net',
    description='Pippin',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Testing",
    ],
    python_requires='>= 3.6',
    setup_requires=[
        'pytest-runner',
        'pip-pin',
    ],
    install_requires=[
    ],
    tests_require=[
        'pytest',
    ],
    develop_requires=[
        'black',
        'isort',
    ],
    entry_points={
        "distutils.commands": [
            "sync = pip_pin:Sync",
            "pin = pip_pin:Pin",
        ],
        "distutils.setup_keywords": [
            "develop_requires = pip_pin:validate_develop_requires",
        ],
        'egg_info.writers': [
            'tests_require.txt = pip_pin:tests_require',
            'develop_requires.txt = pip_pin:develop_requires',
        ],
    },
)
# fmt: on
