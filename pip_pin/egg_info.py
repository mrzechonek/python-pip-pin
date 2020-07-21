def tests_require(cmd, basename, filename):
    cmd.write_file("tests_require", filename, "\n".join(cmd.distribution.tests_require or []))


def develop_requires(cmd, basename, filename):
    try:
        reqs = cmd.distribution.develop_requires or []
    except AttributeError:
        reqs = []

    cmd.write_file("develop_requires", filename, "\n".join(reqs))
