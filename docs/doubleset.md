# DoubleSet

::: doubleset.DoubleSet

## Usage

`DoubleSet` is like a `set`, except it can have up to two of a given element.

```python linenums="1"
from doubleset import DoubleSet
a = DoubleSet({1: 2, 2: 1, 3: 2})
```

Checking membership is still a O(1) operation

```python linenums="3"
print(1 in a)
# True

print(4 in a)
# False
```

When iterating through the elements of a `DoubleSet`, you can see

```python linenums="8"
print(list(sorted(a)))
# [1, 1, 2, 3, 3]
```

## Max Count

## Non-Positive Counts

```python linenums="1"

```

## Addition

TODO

## Subtraction

TODO
