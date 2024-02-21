import inspect
from typing import Callable

from runloop.manifest.manifest import FunctionDescriptor, RunloopParameter, runloop_manifest
from runloop.typing import make_runloop_parameter, make_runloop_return_type


def _make_function_descriptor(func: Callable, parameters: list[RunloopParameter], return_type) -> FunctionDescriptor:
    module = "" if func.__module__ is None else func.__module__
    return FunctionDescriptor(
        name=func.__name__,
        module=module,
        parameters=parameters,
        return_type=return_type,
    )


def function(func: Callable) -> Callable:
    """Register Runloop function.

    Raises
    ------
        ValueError: If function signature is invalid
    """
    parameter_values = inspect.signature(func).parameters.values()
    params = [make_runloop_parameter(param.name, param.annotation) for param in parameter_values]

    return_type = make_runloop_return_type(inspect.signature(func).return_annotation)
    runloop_manifest.register_function(_make_function_descriptor(func, params, return_type))

    return func
