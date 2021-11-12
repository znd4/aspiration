import re

from hypothesis import given, strategies as st
from typer.testing import CliRunner

from casechange.cli import app

runner = CliRunner()


@given(st.text(), st.integers())
def test_script_good_input(s, n):
    """I've used hypothesis a few times. It's ocassionally a bit hard to fit it into a
    test suite, but it seems perfect for this usecase.
    """
    # TODO - Add logic to handle / test bad inputs
    result = runner.invoke(app, [s, str(n)], catch_exceptions=False)

    r = result.stdout

    assert r.lower() == s.lower()

    assert_alphanumerics_match_capitalization_pattern(r, n)


def assert_alphanumerics_match_capitalization_pattern(r: str, n: int):
    pattern = re.compile("([a-z0-9]{%i}[A-Z0-9])*" % (n - 1))
    assert pattern.fullmatch(just_alphanumeric(r))


def just_alphanumeric(s: str) -> str:
    """Replace all non-alphanumeric characters with the empty string"""
    pattern = re.compile(r"[^a-zA-Z0-9]")
    return pattern.sub("", s)
