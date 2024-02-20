from typing import Generic, TypeVar

T = TypeVar("T")


class Session(Generic[T]):
    """A Runloop `Session` is a scoped context within your program.
    Each `Session` has a unique key-value storage to store active runtime state.
    To manage and share state across your executions, add a `Session` parameter to your runloop
    function. Create a `Session` using the runloop API and pass the `id` along with your request
    to invoke your execution.
    Examples include threaded chat history or user preferences.
    TODO: Consider private constructor.
    """

    def __init__(self, id: str, kv: T):
        self.kv: T = kv
        self.id: str = id
