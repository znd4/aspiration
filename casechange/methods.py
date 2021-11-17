import re
import regex


def naive(s: str, n: int) -> str:
    """Loop through the characters in s, constructing a new string
    at each step in the loop. This is probably $O(N^2)$
    """
    s = _strip_null_characters(s)
    alphanumeric_index = 0
    alnum_pattern = regex.compile(
        r"""
            [0-9]
            | # OR
            (?=\p{Alphabetic})      # Letters
            (?=\p{Script=Latin})    # That are also latin
            [^ß] # And not one of these blacklisted characters
        """,
        regex.VERBOSE,
    )
    for i, char in enumerate(s):
        if alnum_pattern.match(char):
            alphanumeric_index = (alphanumeric_index + 1) % n
            if alphanumeric_index:
                s = s[:i] + s[i].lower() + s[i + 1 :]
            else:
                s = s[:i] + s[i].upper() + s[i + 1 :]
    return s


def numpy(s: str, n: int) -> str:
    """Convert `s` into a numpy `char` array.
    Find the indices of the alphanumeric characters, apply `lower`
    and `upper` to those indices according to `n`, and then consolidate
    the array into a single string.

    I haven't profiled this yet, but I expect this to be much faster than naive.

    ### Scaling

    This has a constant number of $O(N)$ numpy operations, so it's $O(N)$

    ### Numpy is compiled

    There isn't a python for loop in sight (numpy is written in C)

    ### Numpy is vectorized

    Because this uses numpy, many of the operations involved here are performed in
    parallel.
    """
    # importing numpy inside a function isn't great, because the import
    # takes a really long time. The import process only needs to happen once,
    # but it's better if it happens at startup, for consistency reasons.
    # However, I'm not sure of a better approach, since numpy is an optional
    # dependency

    s = _strip_null_characters(s)

    import numpy as np

    s_arr = np.array(list(s), dtype=str)

    alnums = _get_alnum_indices_from_str(s)
    # alnums = _get_alphanumerics(s_arr)

    is_not_nth = (np.arange(alnums.shape[0]) + 1) % n

    lowers = alnums[np.where(is_not_nth)]
    uppers = alnums[np.where(np.logical_not(is_not_nth))]

    s_arr[uppers] = np.char.upper(s_arr[uppers])
    s_arr[lowers] = np.char.lower(s_arr[lowers])

    return "".join(s_arr)


def _get_alnum_indices_from_str(s: str):
    # Okay, I'm surrendering to looping with a regular expression
    import numpy as np

    pattern = regex.compile(
        r"""
            [0-9]
            | # OR
            (?=\p{Alphabetic})      # Letters
            (?=\p{Script=Latin})    # That are also latin
            [^ß] # And not one of these blacklisted characters
        """,
        regex.VERBOSE,
    )

    matches = pattern.finditer(s)

    return np.array([m.start() for m in matches], dtype=int)


def _get_alphanumerics(s_arr):
    """Get the lowercase and uppercase letters, and digits"""
    import numpy as np

    return np.where(
        np.logical_and.reduce(
            [
                np.logical_or.reduce(
                    [
                        np.char.islower(s_arr),
                        np.char.isupper(s_arr),
                        np.char.isdigit(s_arr),
                    ]
                ),
                # the small latin characters get counted as non-letters
                *[s_arr != char for char in "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘꞯʀꜱᴛᴜᴠᴡʏᴢ"],
            ]
        )
    )[0]


def _strip_null_characters(s: str):
    pattern = re.compile(r"\x00")
    return pattern.sub("", s)
