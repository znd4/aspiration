from typer import Typer

app = Typer()


@app.command()
def main(string: str, n: int) -> str:
    """Augment string so that every `n`th alphanumeric character is capitalized.

    $ casechange Abc*-2fr 3
    abC*-2fR
    $ casechange r1.abB 2
    r1.aBb
    """
