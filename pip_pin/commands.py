import distutils.cmd
import os
import sys
from contextlib import suppress
from copy import copy
from enum import Enum

from pkg_resources import DistributionNotFound, Requirement, get_distribution

PIP_PIN_DIR = "./.pip-pin"


class Env(Enum):
    INSTALL = "install"
    TESTS = "tests"
    DEVELOP = "develop"

    @property
    def path(self):
        return f"./{PIP_PIN_DIR}/{self.value}.txt"


class Command(distutils.cmd.Command):
    user_options = [
        ("install", "i", "Use install dependencies"),
        ("tests", "t", "Use test dependencies"),
        ("develop", "d", "Use develop dependencies"),
    ]

    def initialize_options(self):
        self.install = False
        self.tests = False
        self.develop = False

    def finalize_options(self):
        self.install = self.install or not any([self.tests, self.develop])

    @property
    def envs(self):
        if self.tests:
            yield Env.TESTS

        if self.develop:
            yield Env.DEVELOP

        if self.install:
            yield Env.INSTALL

    @property
    def reqs(self):
        def parse(reqs):
            return [Requirement.parse(r) for r in reqs]

        return {
            Env.INSTALL: parse(self.distribution.install_requires),
            Env.TESTS: parse(self.distribution.tests_require),
            Env.DEVELOP: parse(self.distribution.develop_requires),
        }


class Sync(Command):
    description = "Pippin sync"

    def initialize_options(self):
        super().initialize_options()

    def run(self):
        cmd = [
            sys.executable,
            "-m",
            "pip",
            "install",
        ]

        for env in self.envs:
            self.announce(f"{env.value}: -r {env.path}")
            cmd += ["-r", os.path.abspath(env.path)]

        self.spawn(cmd)


class Pin(Command):
    description = "Pippin pin"

    def walk(self, req, pins, extras=True):
        # don't pin setuptools
        if req.name == "setuptools":
            return

        dist = get_distribution(req.name)

        pins.update(
            {
                self.walk(r, pins, extras)
                for r in dist.requires(extras=req.extras if extras else [])
            }
        )

        # ignore version if req specifies a direct url
        req.specifier = dist.as_requirement().specifier if req.url is None else None
        req.marker = None
        if not extras:
            req.extras = []
        return req

    def constraints(self):
        constraints = set()

        for env in Env:
            for r in self.reqs[env]:
                constraints.add(self.walk(copy(r), constraints, extras=False))

        constraints = list(sorted(set(str(c) for c in constraints if c)))

        if self.dry_run:
            sys.stderr.write(f"# ./{PIP_PIN_DIR}/constraints.txt\n")
            sys.stderr.write("\n".join(pins))
            sys.stderr.write("\n")
            return

        with open(f"./{PIP_PIN_DIR}/constraints.txt", "w") as f:
            f.write("\n".join(constraints))
            f.write("\n")

    def requirements(self, env):
        pins = set()

        for r in self.reqs[env]:
            pins.add(self.walk(r, pins))

        self.announce(f"# {env.path}")

        pins = list(sorted(set(str(p) for p in pins if p)))
        for pin in pins:
            self.announce(pin)

        if self.dry_run:
            sys.stderr.write(f"# {env.path}\n")
            sys.stderr.write("\n".join(pins))
            sys.stderr.write("\n")
            return

        with open(env.path, "w") as f:
            if env != Env.INSTALL:
                f.write(f"-c constraints.txt\n")

            if env == Env.TESTS:
                f.write(f"-r install.txt\n")
            if env == Env.DEVELOP:
                f.write(f"-r tests.txt\n")

            f.write("\n".join(pins))
            f.write("\n")

    def run(self):
        with suppress(FileExistsError):
            os.mkdir(PIP_PIN_DIR)

        self.constraints()

        for env in self.envs:
            self.requirements(env)


def validate_develop_requires(*args):
    pass
