import string

ALPHANUMERICS = {*string.ascii_letters, *string.digits}


def naive(s: str, n: int) -> str:
    alphanumeric_index = 0
    for i, char in enumerate(s):
        if char in ALPHANUMERICS:
            alphanumeric_index = (alphanumeric_index + 1) % n
            if alphanumeric_index:
                s = s[:i] + s[i].lower() + s[i + 1 :]
            else:
                s = s[:i] + s[i].upper() + s[i + 1 :]
    return s
