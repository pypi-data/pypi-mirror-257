from inspect import Signature
from typing import Any, Type, Union, get_args, get_origin

from pydantic import BaseModel

from runloop.manifest.manifest import (
    ArrayType,
    DictionaryType,
    ModelChildren,
    RunloopParameter,
    RunloopType,
    SessionType,
)

from .session import Session

# Representation of types as strings
_string_type_literal = "string"
_int_type_literal = "int"
_bool_type_literal = "boolean"
_array_type_literal = "array"
_dict_type_literal = "dictionary"
_model_type_literal = "model"
# null type allowed only as return types
_null_type_literal = "null"
_session_type_literal = "session"

_scalar_type_map = {
    str: _string_type_literal,
    int: _int_type_literal,
    bool: _bool_type_literal,

    # NOTE: not supported: bytes, bytearray, set, tuple, float
}
# Instance of supported scalar types
_supported_scalars = [str, int, bool]
# Type annotation for supported scalar types
_supported_scalar_type = Union[Type[str], Type[int], Type[bool]]


def _make_dictionary_parameter(name: str, annotation: Type[Any]) -> RunloopParameter:
    key_type, value_type = get_args(annotation)
    return RunloopParameter(name=name,
                            annotation=annotation,
                            type=_dict_type_literal,
                            dictionary=DictionaryType(key_type=_scalar_type_map[key_type],
                                                      value_type=_make_runloop_type(value_type)))


def _make_scalar_type(param_type: _supported_scalar_type) -> RunloopType:
    if param_type not in _supported_scalars:
        raise TypeError(f"Unsupported Runloop type={param_type}")
    return RunloopType(type_name=_scalar_type_map[param_type],
                       annotation=param_type)


def _make_array_type(annotation: type[Any]) -> RunloopType:
    type_args = get_args(annotation)
    if len(type_args) != 1:
        raise TypeError(f"list type must have key and value type annotations={annotation}")

    return RunloopType(type_name=_array_type_literal,
                       annotation=annotation,
                       array=ArrayType(element_type=_make_runloop_type(type_args[0])))


def _make_dict_type(annotation: type[Any]) -> RunloopType:
    type_args = get_args(annotation)
    if len(type_args) != 2:
        raise TypeError(f"dict type must have key and value type annotations={annotation}")

    if type_args[0] not in _supported_scalars:
        raise TypeError(f"dict key type must be one simple supported type={_supported_scalars}")

    return RunloopType(type_name=_dict_type_literal,
                       annotation=annotation,
                       dictionary=DictionaryType(key_type=_make_runloop_type(type_args[0]),
                                                 value_type=_make_runloop_type(type_args[1])))


def _make_model_type(annotation: type[Any]) -> RunloopType:
    children = [make_runloop_parameter(field_name, field_info.annotation)
                for (field_name, field_info) in annotation.__fields__.items()]
    return RunloopType(type_name=_model_type_literal, annotation=annotation, model=ModelChildren(children=children))


def _make_session_type(annotation: type[Any]) -> RunloopType:
    session_type = get_args(annotation)
    kv_type = _make_runloop_type(session_type[0])
    # TODO: Session parsing incomplete
    return RunloopType(type_name=_session_type_literal, annotation=Session, session=SessionType(kv_type=kv_type))


def _make_runloop_type(annotation: Type[Any]) -> RunloopType:
    if annotation is None:
        raise TypeError("type of None not supported, type must be annotated")

    origin = get_origin(annotation)
    if origin is None:
        if annotation in _supported_scalars:
            return _make_scalar_type(annotation)
        elif issubclass(annotation, BaseModel):
            return _make_model_type(annotation)
        elif annotation == dict:
            # dict without type hints, ie dict class
            raise TypeError("dict type must explicitly declare key value types")
        elif annotation == list:
            # list without type hints, ie dict class
            raise TypeError("list type must explicitly declare key value types")
    elif origin == Session:
        return _make_session_type(annotation)
    elif origin == list:
        return _make_array_type(annotation)
    elif origin == dict:
        return _make_dict_type(annotation)
    else:
        raise TypeError(f"Unsupported Runloop type={annotation}")


def make_runloop_parameter(name: str, annotation: Type[Any]) -> RunloopParameter:
    return RunloopParameter(name=name, type=_make_runloop_type(annotation))


def make_runloop_return_type(annotation: Type[Any]) -> RunloopType:
    # none type supported for return types only, where annotation is None (explicit)
    # or annotation is Signature.empty (omitted)
    if annotation is None or annotation == Signature.empty:
        return RunloopType(type_name=_null_type_literal)
    return _make_runloop_type(annotation)
