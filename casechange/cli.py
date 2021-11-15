import typer
from enum import Enum
from .methods import naive, numpy
from typing import Literal

app = typer.Typer(add_completion=False)


class Method(str, Enum):
    naive = "naive"
    numpy = "numpy"


@app.command()
def main(string: str, n: int, method: Method = Method.naive):
    """Augment `string` so that every `n`th alphanumeric character is capitalized.

    ```sh
    $ casechange Abc*-2fr 3
    abC*-2fR

    $ casechange r1.abB 2
    r1.aBb
    ```
    """
    if method == Method.naive:
        result = naive(string, n)
    if method == Method.numpy:
        result = numpy(string, n)
    else:
        raise NotImplementedError(f"Have not implemented {method=}")

    typer.echo(result)


# This is added for documentation purposes (the mkdocs-click plugin needs access to the
# underlying click app)
click_app = typer.main.get_command(app)
