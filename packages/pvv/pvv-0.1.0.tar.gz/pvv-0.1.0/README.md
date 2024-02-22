# pvv

Minimal Python decorator to enforce type validation from type hints

## Installation

This library has been created to have zero dependencies, and work with native Python. Use your favorite package manager to install `pvv` from PyPI.

```
pip install pvv
```

## Usage

There are two ways to use the `validate` decorator from `pvv`:

### Validate all parameters

Just use the decorator. A `TypeError` will be raised if the function is called with parameters of incorrect type.

> NOTE: `pvv` will check if the given parameters to a function are instances of the class annotated as a parameter. If one parameter has no type hints, it will be ignored in the validation.

```python
from pvv import validate

@validate
def function(a: str, b: int, c):
    pass
```

```
>>> function("a", 3, 2)
>>> function(c=2, a="a", b=2)
>>> function(3, "a", 2)
TypeError: Incorrect type of function arguments: 'a' must be of type 'str', 'b' must be of type 'int'
```

### Validate some parameters

```python
from pvv import validate

@validate('a', 'c')
def function(a: str, b: int, c: bool | None):
    pass
```

```
>>> function("a", 3, True)
>>> function(3, "b", 0)
TypeError: Incorrect type of function arguments: 'a' must be of type 'str', 'c' must be of type 'bool | None'
```

### An important note

The parameters of the `validate` decorator must all be of type `str`, otherwise a `ValidatorError` will be raised:

```
>>> @validate('a', 1)
... def func(*args, **kwargs):
...     pass
pvv.exceptions.ValidatorError: All arguments of decorator must be of type 'str'
```
