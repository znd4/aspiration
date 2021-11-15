import re

import pytest
from hypothesis import example, given, strategies as st, target
from typer.testing import CliRunner

from casechange.cli import app

runner = CliRunner()


@pytest.mark.timeout(30)
@pytest.mark.parametrize("method", ["naive", "numpy"])
@given(
    # We need to blacklist "\r"
    s=st.text(st.characters(blacklist_categories=("Cs",), blacklist_characters="\r")),
    n=st.integers(min_value=1),
)
@example("Ab.d3", 2)  # should return "aB.d3"
def test_script_good_input(method: str, s: str, n: int):
    """I've used hypothesis a few times. It's ocassionally a bit hard to fit it into a
    test suite, but it seems perfect for this usecase.
    """
    # At some point, hypothesis failed to come up with a simple failure condition
    # ( e.g. @example("Ab.c1", 2) )
    # Here we're trying to get hypothesis to pick strings with a good mix of lowercase,
    # uppercase, and non-letters.
    target(
        len(just_lowercase(s))
        * len(just_uppercase(s))
        * len(just_nonletters(s))
        / (len(s) + 1) ** 3
    )

    result = runner.invoke(
        app, [s, str(n), f"--method={method}"], catch_exceptions=False
    )

    # stdout includes an extra newline suffix
    r = result.stdout.removesuffix("\n")

    # ignoring capitalization, the input and output strings should be thesame
    assert r.lower() == s.lower()

    assert_alphanumerics_match_capitalization_pattern(r, n)


def assert_alphanumerics_match_capitalization_pattern(r: str, n: int):
    """
    Remove all non-alphanumeric characters, then check if the remaining characters fit the
    required capitalization pattern
    """
    alphanumerics = just_alphanumeric(r)
    if n > len(alphanumerics):  # added due to sre_parse.MAX_REPEAT limit
        return

    pattern = re.compile(
        """
            (
                [a-z0-9]{%i}    # n-1 lowercase characters
                [A-Z0-9]        # followed by one uppercase character
            )*                  # We can have {0, 1, 2, ...} n-grams.
            # The alphanumerics can end in 0 to n-1 lowercase characters.
            [a-z0-9]{0,%i}
        """
        % (n - 1, n - 1),
        re.VERBOSE,
    )
    assert pattern.fullmatch(alphanumerics)


def just_nonletters(s: str) -> str:
    pattern = re.compile(r"[^a-zA-Z]")
    return pattern.sub("", s)


def just_lowercase(s: str) -> str:
    pattern = re.compile(r"[^a-z]")
    return pattern.sub("", s)


def just_uppercase(s: str) -> str:
    pattern = re.compile(r"[^A-Z]")
    return pattern.sub("", s)


def just_alphanumeric(s: str) -> str:
    """Replace all non-alphanumeric characters with the empty string"""
    pattern = re.compile(r"[^a-zA-Z0-9]")
    return pattern.sub("", s)
