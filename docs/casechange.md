# Case Change

::: mkdocs-click
    :module: casechange.cli
    :command: click_app
    :depth: 1

## Installation

If you're okay with using the default `naive` method, you can use the standard [installation instructions](./getting_started.md). However, if you want to use the more efficient `numpy` method, you'll need to include the `[numpy]` extra (and also have the depencies for installing numpy, which vary from platform to platform).

```sh
# I couldn't get `aspiration[numpy]` working with a git url install
pip install numpy "git+https://github.com/zdog234/aspiration.git@main"
```

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
