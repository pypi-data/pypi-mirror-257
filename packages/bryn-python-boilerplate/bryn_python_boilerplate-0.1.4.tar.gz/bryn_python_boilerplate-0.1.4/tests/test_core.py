"""Tests for `python_boilerplate` package."""

from python_boilerplate import core


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    print(core.__file__)
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
