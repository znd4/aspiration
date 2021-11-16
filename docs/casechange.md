# Case Change

::: mkdocs-click
    :module: casechange.cli
    :command: click_app
    :depth: 1

## Edge-Cases

### "\r"

Including `\r` in a string isn't tested, because a solitary `\r` the `typer` test runner isn't able to capture it (at least on my MacOS / linux environments). (This was discovered by hypothesis)

### "\x00"

Null bytes will be removed before processing. I don't know of a better way to handle them because I don't understand their behavior. (a solitary `"\x00"` gets stripped when)

## Methods

There are multiple implementations of the casechange algorithm. These can be selected with the `--method` flag.

### numpy

::: casechange.methods.numpy

### naive

::: casechange.methods.naive
