import string

import typer

app = typer.Typer()

ALPHANUMERICS = {*string.ascii_letters, *string.digits}


@app.command()
def main(s: str, n: int):
    """Augment `s` so that every `n`th alphanumeric character is capitalized.

    $ casechange Abc*-2fr 3
    abC*-2fR
    $ casechange r1.abB 2
    r1.aBb
    """

    alphanumeric_index = 0
    for i, char in enumerate(s):
        if char in ALPHANUMERICS:
            alphanumeric_index = (alphanumeric_index + 1) % n
            if alphanumeric_index:
                s = s[:i] + s[i].lower() + s[i + 1 :]
            else:
                s = s[:i] + s[i].upper() + s[i + 1 :]
    typer.echo(s)
