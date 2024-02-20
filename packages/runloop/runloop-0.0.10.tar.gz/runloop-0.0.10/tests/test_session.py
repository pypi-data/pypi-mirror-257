from pydantic import BaseModel

from runloop import Session


def test_runloop_return_type_simple():
    class Thread(BaseModel):
        name: str
        message_count: int

    session = Session(id="whatisthis", kv=Thread(name="test", message_count=234))
    assert session.kv.name == "test"
    assert session.kv.message_count == 234


def test_runloop_return_type_dict():
    session = Session(id="thisId", kv={"name": "test", "message_count": 234})
    assert session.kv["name"] == "test"
    assert session.kv["message_count"] == 234
