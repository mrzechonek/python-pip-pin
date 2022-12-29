from pip_pin import util


def tests_require(cmd, basename, filename):
    cmd.write_file(
        "tests_require", filename, "\n".join(util.get_tests_require(cmd.distribution))
    )


def develop_requires(cmd, basename, filename):
    cmd.write_file(
        "develop_requires",
        filename,
        "\n".join(util.get_develop_requires(cmd.distribution)),
    )
