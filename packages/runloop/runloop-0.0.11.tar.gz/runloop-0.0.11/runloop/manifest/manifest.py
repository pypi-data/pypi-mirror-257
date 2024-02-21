from typing import Any, List, TypeVar, Union

from pydantic import BaseModel, Field

# forward declaration
RunloopParameter = TypeVar("RunloopParameter")
RunloopType = TypeVar("RunloopType")


class DictionaryType(BaseModel):
    key_type: RunloopType
    value_type: RunloopType


class ModelChildren(BaseModel):
    children: List[RunloopParameter]


class ArrayType(BaseModel):
    element_type: RunloopType


class SessionType(BaseModel):
    kv_type: RunloopType


class RunloopType(BaseModel):
    type_name: str
    # TODO: Ensure continued compatibility among supported python versions
    annotation: Any = Field(None, exclude=True)
    dictionary: Union[None | DictionaryType] = None
    array: Union[None | ArrayType] = None
    model: Union[None | ModelChildren] = None
    session: Union[None | SessionType] = None


class RunloopParameter(BaseModel):
    name: str
    type: RunloopType


class FunctionDescriptor(BaseModel):
    name: str
    module: str
    parameters: List[RunloopParameter]
    return_type: RunloopType


class RunloopManifest(BaseModel):
    functions: List[FunctionDescriptor] = []

    def register_function(self, function: FunctionDescriptor):
        self.functions.append(function)


runloop_manifest: RunloopManifest = RunloopManifest()
