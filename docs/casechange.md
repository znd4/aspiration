# Case Change

::: mkdocs-click
:module: casechange.cli
:command: click_app
:depth: 1

## Edge-Cases

### "\r"

Including `\r` in a string isn't tested, because a solitary `\r` the `typer` test runner isn't able to capture it (at least on my MacOS / linux environments). (This was discovered by hypothesis)

## Some other section
