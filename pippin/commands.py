import distutils.cmd
import operator
import subprocess
import sys
from enum import Enum
from functools import reduce

from pkg_resources import DistributionNotFound, Requirement, get_distribution


class Env(Enum):
    INSTALL = "install"
    TESTS = "tests"
    DEVELOP = "develop"


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

    user_options = Command.user_options + [
        ("pinned", "p", "Install pinned versions"),
    ]

    def initialize_options(self):
        super().initialize_options()
        self.pinned = False

    def run(self):
        cmd = [
            sys.executable,
            "-m",
            "pip",
            "install",
        ]

        for env in self.envs:
            if self.pinned:
                subprocess.check_call(
                    cmd + ["-r", f".pippin.{env.value}",]
                )

            else:
                subprocess.check_call(cmd + [str(r) for r in self.reqs[env]])


class Pin(Command):
    description = "Pippin pin"

    def walk(self, req, pins):
        dist = get_distribution(req.name)

        pins.update({self.walk(r, pins) for r in dist.requires(extras=req.extras)})

        req.specifier = dist.as_requirement().specifier
        req.marker = None
        return req

    def run(self):
        for env in self.envs:
            pins = set()

            try:
                for r in self.reqs[env]:
                    pins.add(self.walk(r, pins))
            except DistributionNotFound:
                raise RuntimeError("Run setup.py sync first") from None

            with open(".pippin.%s" % env.value, "w") as f:
                if env == Env.TESTS:
                    f.write("-c .pippin.install\n")
                if env == Env.DEVELOP:
                    f.write("-c .pippin.tests\n")

                f.write("\n".join(sorted(map(str, pins))))
                f.write("\n")


def validate_develop_requires(*args):
    pass
