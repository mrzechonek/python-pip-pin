#!env python

from setuptools import find_packages, setup

# fmt: off
setup(
    name='pippin',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/mrzechonek/pippin',
    license='MIT',
    author='Michał Lowas-Rzechonek',
    author_email='michal@rzechonek.net',
    description='Pippin',
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
            "sync = pippin:Sync",
            "pin = pippin:Pin",
        ],
        "distutils.setup_keywords": [
            "develop_requires = pippin:validate_develop_requires",
        ],
        'egg_info.writers': [
            'tests_require.txt = pippin:tests_require',
            'develop_requires.txt = pippin:develop_requires',
        ],
    },
)
# fmt: on
