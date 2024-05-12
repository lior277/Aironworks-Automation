import pytest


def common_resource(name):
    "mark tests as using a common resource named 'name', cause the test to not run in parallel"
    return pytest.mark.xdist_group(name=name)
