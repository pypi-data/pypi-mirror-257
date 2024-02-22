import inspect
from typing import Any, Callable

from .exceptions import ValidatorError


def validate(*args: str):
    """Validate function parameters

    This decorator is used to enforce validation of a function's type hints

    Args:
        *args (str): names of functions parameters to be validated

    Raises:
        TypeError: when one or more of the type validations fail
            (will also notify of the parameters with incorrect types)
        ValidatorError: when the decorator has incorrect parameters
            (all parameters must be of type string)
    """

    def _validate_input(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            parameters_validate = decorator_args

            # retrieve function signature
            signature = inspect.signature(func)

            # bind passed arguments to the function signature
            bound_arguments = signature.bind(*args, **kwargs)
            bound_arguments.apply_defaults()

            # check type annotations
            wrong_types = []
            for name, value in bound_arguments.arguments.items():
                # for parameters we want to validate
                if (not parameters_validate) or (name in parameters_validate):
                    parameter = signature.parameters[name]
                    if parameter.annotation != inspect.Parameter.empty:
                        if not isinstance(value, parameter.annotation):
                            parameter_name = (
                                parameter.__name__
                                if "__name__" in dir(parameter)
                                else str(parameter).split(": ")[1]
                            )
                            wrong_types.append((name, parameter_name))

            if wrong_types:
                raise TypeError(
                    "Incorrect type of function argument"
                    + ("s: " if len(wrong_types) > 1 else ": ")
                    + ", ".join(
                        [f"'{it[0]}' must be of type '{it[1]}'" for it in wrong_types]
                    )
                )

            return func(*args, **kwargs)

        return wrapper

    # make this decorator callable with or without parameters,
    # i.e., @validate_input, @validate_input() or @validate_input('param1', 'param2', ...)
    if len(args) == 1 and callable(args[0]):
        # no decorator arguments, we set decorator arguments to an empty tuple
        decorator_args = ()
        return _validate_input(args[0])
    else:
        # has decorator, we check all parameters are of type string
        if not all(isinstance(item, str) for item in args):
            raise ValidatorError("All arguments of decorator must be of type 'str'")
        decorator_args = args
        return _validate_input
