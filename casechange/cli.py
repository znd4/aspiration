import string as string_

import typer

app = typer.Typer(add_completion=False)


# rename so that we can use the argument name string in main
ALPHANUMERICS = {*string_.ascii_letters, *string_.digits}


@app.command()
def main(sequence: str, n: int):
    """Augment `sequence` so that every `n`th alphanumeric character is capitalized.

    ```sh
    $ casechange Abc*-2fr 3
    abC*-2fR

    $ casechange r1.abB 2
    r1.aBb
    ```
    """

    alphanumeric_index = 0
    for i, char in enumerate(sequence):
        if char in ALPHANUMERICS:
            alphanumeric_index = (alphanumeric_index + 1) % n
            if alphanumeric_index:
                sequence = sequence[:i] + sequence[i].lower() + sequence[i + 1 :]
            else:
                sequence = sequence[:i] + sequence[i].upper() + sequence[i + 1 :]
    typer.echo(sequence)


# This is added for documentation purposes (the mkdocs-click plugin needs access to the
# underlying click app)
click_app = typer.main.get_command(app)
