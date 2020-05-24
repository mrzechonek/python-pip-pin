import distutils
import subprocess
import sys
from enum import Enum

from pkg_resources import Requirement, get_distribution


class Environment(Enum):
    INSTALL = "install"
    TESTS = "tests"
    DEVELOP = "develop"


class Command(distutils.cmd.Command):
    user_options = [
        ("tests", "t", "Use test dependencies"),
        ("develop", "d", "Use develop dependencies"),
    ]

    def initialize_options(self):
        self.install = True
        self.tests = False
        self.develop = False

    def finalize_options(self):
        assert not (self.tests and self.develop), "Can't do both"

    def get_reqs(self, pinned=False):
        reqs = {
            Environment.INSTALL: self.distribution.install_requires,
            Environment.TESTS: self.distribution.tests_require,
            Environment.DEVELOP: self.distribution.develop_requires,
        }

        if not pinned:
            return reqs[self.environment]

        raise NotImplementedError("sync --pinned")

    @property
    def environment(self):
        if self.tests:
            return Environment.TESTS

        if self.develop:
            return Environment.DEVELOP

        return Environment.INSTALL


class Sync(Command):
    description = "Pippin sync"

    user_options = Command.user_options + [
        ("pinned", "p", "Install pinned versions"),
    ]

    def initialize_options(self):
        super().initialize_options()
        self.pinned = False

    def run(self):
        self.announce("Syncing %s" % (self.environment))

        # TODO: pip options?
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install"] + self.get_reqs()
        )


class Pin(Command):
    description = "Pippin pin"

    def run(self):
        # TODO: recursively pin what's currently installed into .ini sections
        raise NotImplementedError("pin")
        self.announce("Pinning %s" % (self.environment))


def validate_develop_requires(*args):
    pass
