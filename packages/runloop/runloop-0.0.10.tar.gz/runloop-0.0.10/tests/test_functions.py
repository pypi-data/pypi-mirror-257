from pydantic import BaseModel
from pytest import raises


def test_runloop_function_simple_scalars():
    from runloop import function, runloop_manifest

    @function
    def fn1(name: str, age: int) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn1"][0]
    assert len(runloop_manifest.functions) > 0
    assert test_fns.name == "fn1"
    assert test_fns.module == "tests.test_functions"
    assert len(test_fns.parameters) == 2
    assert test_fns.parameters[0].name == "name"
    assert test_fns.parameters[0].type.type_name == "string"
    assert test_fns.parameters[1].name == "age"
    assert test_fns.parameters[1].type.type_name == "int"


def test_runloop_function_simple_model():
    from runloop import function, runloop_manifest

    class Simple(BaseModel):
        height: str
        weight: int

    @function
    def fn2(name: str, m1: Simple) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn2"][0]
    assert len(runloop_manifest.functions) > 0
    assert test_fns.name == "fn2"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 2
    assert test_fns.parameters[0].name == "name"
    assert test_fns.parameters[0].type.type_name == "string"
    assert test_fns.parameters[1].name == "m1"
    # Validate children
    assert len(test_fns.parameters[1].type.model.children) == 2
    assert test_fns.parameters[1].type.model.children[0].name == "height"
    assert test_fns.parameters[1].type.model.children[0].type.type_name == "string"
    assert test_fns.parameters[1].type.model.children[1].name == "weight"
    assert test_fns.parameters[1].type.model.children[1].type.type_name == "int"


def test_runloop_function_nested_model():
    from runloop import function, runloop_manifest

    class Simple(BaseModel):
        height: str
        weight: int

    class Nested(BaseModel):
        simple: Simple
        name: str

    @function
    def fn3(name: str, m1: Nested) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn3"][0]
    assert len(runloop_manifest.functions) > 0
    assert test_fns.name == "fn3"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 2
    assert test_fns.parameters[0].name == "name"
    assert test_fns.parameters[0].type.type_name == "string"
    assert test_fns.parameters[1].name == "m1"
    assert test_fns.parameters[1].type.type_name == "model"
    # Validate children
    assert len(test_fns.parameters[1].type.model.children) == 2
    assert test_fns.parameters[1].type.model.children[0].name == "simple"
    assert test_fns.parameters[1].type.model.children[0].type.type_name == "model"
    assert len(test_fns.parameters[1].type.model.children[0].type.model.children) == 2
    assert test_fns.parameters[1].type.model.children[0].type.model.children[0].name == "height"
    assert test_fns.parameters[1].type.model.children[0].type.model.children[0].type.type_name == "string"
    assert test_fns.parameters[1].type.model.children[0].type.model.children[1].name == "weight"
    assert test_fns.parameters[1].type.model.children[0].type.model.children[1].type.type_name == "int"
    assert test_fns.parameters[1].type.model.children[1].name == "name"
    assert test_fns.parameters[1].type.model.children[1].type.type_name == "string"


def test_runloop_dict_str_str():
    from runloop import function, runloop_manifest

    @function
    def fn4(dict_arg: dict[str, str]) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn4"][0]
    assert len(runloop_manifest.functions) > 0
    assert test_fns.name == "fn4"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 1
    assert test_fns.parameters[0].name == "dict_arg"
    assert test_fns.parameters[0].type.type_name == "dictionary"
    assert test_fns.parameters[0].type.dictionary.key_type.type_name == "string"
    assert test_fns.parameters[0].type.dictionary.value_type.type_name == "string"


def test_runloop_dict_str_simple_model():
    from runloop import function, runloop_manifest

    class Simple(BaseModel):
        height: str
        weight: int

    @function
    def fn5(dict_arg: dict[str, Simple]) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn5"][0]
    assert len(runloop_manifest.functions) > 0
    assert test_fns.name == "fn5"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 1
    assert test_fns.parameters[0].name == "dict_arg"
    assert test_fns.parameters[0].type.type_name == "dictionary"
    assert test_fns.parameters[0].type.dictionary.key_type.type_name == "string"
    assert test_fns.parameters[0].type.dictionary.value_type.type_name == "model"

    # Validate children
    assert len(test_fns.parameters[0].type.dictionary.value_type.model.children) == 2
    assert test_fns.parameters[0].type.dictionary.value_type.model.children[0].name == "height"
    assert test_fns.parameters[0].type.dictionary.value_type.model.children[0].type.type_name == "string"
    assert test_fns.parameters[0].type.dictionary.value_type.model.children[1].name == "weight"
    assert test_fns.parameters[0].type.dictionary.value_type.model.children[1].type.type_name == "int"


def test_runloop_dict_no_types_throws():
    from runloop import function

    with raises(TypeError):
        @function
        def fn6(_: dict) -> int:
            pass


def test_runloop_array_str():
    from runloop import function, runloop_manifest

    @function
    def fn7(array_arg: list[str]) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn7"][0]
    assert test_fns.name == "fn7"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 1
    assert test_fns.parameters[0].name == "array_arg"
    assert test_fns.parameters[0].type.type_name == "array"
    assert test_fns.parameters[0].type.array.element_type.type_name == "string"


def test_runloop_array_nested_model():
    from runloop import function, runloop_manifest

    class Simple(BaseModel):
        height: str
        weight: int

    @function
    def fn8(array_arg: list[Simple]) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn8"][0]
    assert test_fns.name == "fn8"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 1
    assert test_fns.parameters[0].name == "array_arg"
    assert test_fns.parameters[0].type.type_name == "array"
    assert test_fns.parameters[0].type.array.element_type.type_name == "model"

    assert len(test_fns.parameters[0].type.array.element_type.model.children) == 2
    assert test_fns.parameters[0].type.array.element_type.model.children[0].name == "height"
    assert test_fns.parameters[0].type.array.element_type.model.children[0].type.type_name == "string"
    assert test_fns.parameters[0].type.array.element_type.model.children[1].name == "weight"
    assert test_fns.parameters[0].type.array.element_type.model.children[1].type.type_name == "int"


def test_runloop_list_no_types_throws():
    from runloop import function

    with raises(TypeError):
        @function
        def fn9(_: list) -> int:
            pass


def test_runloop_return_type_simple():
    from runloop import function, runloop_manifest

    @function
    def fn10(arg1: int) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn10"][0]
    assert test_fns.name == "fn10"
    assert test_fns.return_type.type_name == "int"

    @function
    def fn11(arg1: int) -> bool:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn11"][0]
    assert test_fns.name == "fn11"
    assert test_fns.return_type.type_name == "boolean"

    @function
    def fn12(arg1: int) -> str:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn12"][0]
    assert test_fns.name == "fn12"
    assert test_fns.return_type.type_name == "string"


def test_runloop_return_type_complex():
    from runloop import function, runloop_manifest

    @function
    def fn_cplx_1(arg1: int) -> list[str]:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_cplx_1"][0]
    assert test_fns.name == "fn_cplx_1"
    assert test_fns.return_type.type_name == "array"
    assert test_fns.return_type.array.element_type.type_name == "string"

    class Simple(BaseModel):
        height: str
        weight: int

    @function
    def fn_cplx_2(arg1: int) -> Simple:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_cplx_2"][0]
    assert test_fns.name == "fn_cplx_2"
    assert test_fns.return_type.type_name == "model"
    assert len(test_fns.return_type.model.children) == 2
    assert test_fns.return_type.model.children[0].name == "height"
    assert test_fns.return_type.model.children[0].type.type_name == "string"
    assert test_fns.return_type.model.children[1].name == "weight"
    assert test_fns.return_type.model.children[1].type.type_name == "int"


def test_runloop_return_type_none():
    from runloop import function, runloop_manifest

    @function
    def fn_empty_1(arg1: int) -> None:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_empty_1"][0]
    assert test_fns.name == "fn_empty_1"
    assert test_fns.return_type.type_name == "null"

    @function
    def fn_empty_2(arg1: int):
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_empty_2"][0]
    assert test_fns.name == "fn_empty_2"
    assert test_fns.return_type.type_name == "null"


def test_runloop_session_parameter():
    from runloop import Session, function, runloop_manifest

    class Thread(BaseModel):
        name: str
        message_count: int

    @function
    def fn_return_session_1(session1: Session[Thread]) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_return_session_1"][0]
    assert test_fns.name == "fn_return_session_1"
    assert test_fns.parameters[0].name == "session1"
    assert test_fns.parameters[0].type.type_name == "session"
    assert test_fns.parameters[0].type.session.kv_type.type_name == "model"
    assert test_fns.parameters[0].type.session.kv_type.model.children[0].name == "name"
    assert test_fns.parameters[0].type.session.kv_type.model.children[0].type.type_name == "string"
    assert test_fns.parameters[0].type.session.kv_type.model.children[1].name == "message_count"
    assert test_fns.parameters[0].type.session.kv_type.model.children[1].type.type_name == "int"
