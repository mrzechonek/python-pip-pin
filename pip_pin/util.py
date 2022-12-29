def get_develop_requires(dist):
    return dist.develop_requires or dist.extras_require.get("develop", [])


def get_tests_require(dist):
    return dist.tests_require or dist.extras_require.get("tests", [])
