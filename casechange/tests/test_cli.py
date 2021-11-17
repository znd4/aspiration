import re
import regex

import pytest
from hypothesis import example, given, strategies as st, target
from typer.testing import CliRunner

from casechange.cli import app

runner = CliRunner()


# @pytest.mark.timeout(30)
@pytest.mark.parametrize("method", ["naive", "numpy"])
@given(
    # We need to blocklist "\r"
    s=st.text(
        st.characters(blocklist_categories=("Cs",), blocklist_characters=("\r", "\x00"))
    ),
    n=st.integers(min_value=1),
)
@example(s="Ab.d3", n=2)  # should return "aB.d3"
@example(s="0Āa", n=2)  # thanks again, hypothesis :)
@example(s="ā", n=1)
# The small capital letters are tricky. They're lowercase and can't be upper-cased
@example(s="ᴀa", n=2)
@example(s="º", n=1)
@example(s="\x00" + "a", n=1)  # Strip null characters (I)
@example(s="აa", n=1)
@example(s="ß", n=1)
def test_script_good_input(method: str, s: str, n: int):
    """I've used hypothesis a few times. It's ocassionally a bit hard to fit it into a
    test suite, but it seems perfect for this usecase.
    """
    # At some point, hypothesis failed to come up with a simple failure condition
    # ( e.g. @example("Ab.c1", 2) )
    # Here we're trying to get hypothesis to pick strings with a good mix of lowercase,
    # uppercase, and non-letters.
    if s.startswith("-"):
        return

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

    s = _strip_null_characters(s)

    # ignoring capitalization, the input and output strings should be thesame
    assert r.lower() == s.lower()

    assert_alphanumerics_match_capitalization_pattern(r, n)


def _strip_null_characters(s: str):
    pattern = re.compile(r"\x00")
    return pattern.sub("", s)


def assert_alphanumerics_match_capitalization_pattern(r: str, n: int):
    """
    Remove all non-alphanumeric characters, then check if the remaining characters fit the
    required capitalization pattern
    """
    alphanumerics = just_alphanumeric(r)
    if n > len(alphanumerics):  # added due to sre_parse.MAX_REPEAT limit
        return

    pattern = regex.compile(
        r"""
            (
                [\p{Ll}\dᴀ-ᴢ]{%i}    # n-1 lowercase characters
                [\p{Lu}\dᴀ-ᴢ]        # followed by one uppercase character
            )*                  # We can have {0, 1, 2, ...} n-grams.
            # The alphanumerics can end in 0 to n-1 lowercase characters.
            [\p{Ll}\dᴀ-ᴢ]{0,%i}
        """
        % (n - 1, n - 1),
        regex.VERBOSE,
    )
    assert pattern.fullmatch(alphanumerics)


def just_nonletters(s: str) -> str:
    pattern = re.compile(r"\w")
    return pattern.sub("", s)


def just_lowercase(s: str) -> str:
    pattern = re.compile(r"[^a-z]")
    return pattern.sub("", s)


def just_uppercase(s: str) -> str:
    pattern = re.compile(r"[^A-Z]")
    return pattern.sub("", s)


def just_alphanumeric(s: str) -> str:
    """Replace all non-alphanumeric characters with the empty string"""
    pattern = regex.compile(
        # This was a total pain to get right.
        r"""
            (?=[^0-9])          # not a number AND ...
            (
                (\P{Latin}|(?=\P{Ll})\P{Lu}) # isn't a latin letter
                | [ß] # isn't one of these blocklisted characters
            )
        """,
        regex.VERBOSE,
    )
    return pattern.sub("", s)
