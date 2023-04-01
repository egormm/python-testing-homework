"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import httpretty
import pytest

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',
    'plugins.identity.user',
    'plugins.identity.placeholder',
]


@pytest.fixture(autouse=True)
def _network_access_restricted():
    """
    This fixture is used to restrict network access for all tests.

    It is used to prevent tests from making real HTTP requests.
    """
    httpretty.enable(allow_net_connect=False, verbose=True)
    yield
    httpretty.disable()
