# Case Change

## Edge-Cases

### "\r"

Including `\r` in a string isn't tested, because a solitary `\r` the `typer` test runner isn't able to capture it (at least on my MacOS / linux environments). (This was discovered by hypothesis)
