# Coding Interview for Aspiration

[Documentation](https://zanedufour-aspiration-wz9eq.ondigitalocean.app/) - hosted on digital ocean behind an oauthproxy2 server. You may need to reach out to `zane@znd4.me` to get access.

[Click here](https://github.com/zdog234/aspiration/edit/main/README.md) to edit this page. (`docs/index.md` is just a simlink to the README)

## Casechange

I decided to implement `casechange` as a CLI. You can check out its page in the docs for more info.

## DoubleSet

`DoubleSet` is implemented as a class that gets instantiated from a `dict`.

```python linenums="1"
from doubleset import DoubleSet
ds = DoubleSet({1: 1, 2: 2})

print(sum(ds))
# 5

print(1 in ds)
# True (O(1) lookup)
```

For more information, check out its page in the docs.

## Pre-requisites

1. [python](https://realpython.com/installing-python/)

## Installation

```sh
pip install git+https://github.com/zdog234/aspiration.git@main
```
