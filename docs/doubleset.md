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

The maximum number of occurrences of an element in a DoubleSet is two

```python linenums="1"
b = DoubleSet({1: 2, 2: 5})

print(list(sorted(b)))
# [1, 1, 2, 2]
```

## Non-Positive Counts

If an element has a nonpositive count, it won't be present in the instantiated `DoubleSet`

```python linenums="1"
c = DoubleSet({1: 0, 2: -20})

print(list(sorted(c)))
# []
```

## Addition

Adding two `DoubleSet`s is defined as adding the counts of each of the equal elements (still with a max count per element of two).

```python linenums="1"
x = DoubleSet({1: 1, 2: 2})
y = DoubleSet({1: 1, 2: 1})

z = x + y
print(list(sorted(z)))
# [1, 1, 2, 2]
```

If an element is present in one `DoubleSet` but not the other, we take the count from the `DoubleSet` where it is present.

```python linenums="1"
x = DoubleSet({1: 1, 2: 1})
y = DoubleSet({2: 1, 3: 1})

z = x + y
print(list(sorted(z)))
# [1, 2, 2, 3]
```

Finally, because a DoubleSet cannot have elements with nonpositive counts, `DoubleSet`s do not have inverses.

For math-ey people: if $S$ is the set of all integer-containing `DoubleSet`s, then

$$
\forall s \in{S} \hspace{1mm} \mid \hspace{1mm} \textnormal{len(}s\textnormal{)>0},\\
\nexists t \in{S} \mid s+t = \emptyset
$$

Here's a code example that might explain this better. What will this output?

```python linenums="1"
x = DoubleSet({1: 1})
y = DoubleSet({1: -1})

z = x + y
print(list(sorted(z)))
```

At first glance, it might look like the `1` and `-1` in the counts should cancel out, such that this would output `[]`, but we actually end up with `[1]`. The reason for this is that `y` is actually the empty set, because any elements with nonpositive counts get ignored.

```python linenums="6"
print(y == DoubleSet({}))
# True
```

## Subtraction

Subtraction of two `DoubleSet`s is _like_ addition -- we subtract the counts of elements in the right `DoubleSet` from the counts of the elements in the left `DoubleSet`.

```python linenums="1"
x = DoubleSet({1: 2})
print("x =", list(sorted(x)))
# x = [1, 1]

y = DoubleSet({1: 1})
print("y =", list(sorted(y)))
# y = [1]

z = x - y
print(list(sorted(z)))
# [1]
```

We need to remember the rule that the count of an element has to be `>0` and `<=2`.

```python linenums="1"
z = DoubleSet({1: 3}) - DoubleSet({1: 2})
print("z = ", list(sorted(z)))
# z = []

z = DoubleSet({1: 1}) - DoubleSet({1: -1})
print("z = ", list(sorted(z)))
# z = [1]
```
