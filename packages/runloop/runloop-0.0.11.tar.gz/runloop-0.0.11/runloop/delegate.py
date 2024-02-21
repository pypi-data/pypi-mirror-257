import abc


class Delegate(abc.ABC):
    """The runloop Delegate is responsible for implementing runloop scheduling / event, storage, and
    observability layers. Once registered, a delegate will receive all runloop initiated events and be responsible
    for implementation of proper implementation of the runloop system.
    """

    @abc.abstractmethod
    def commit_session(self, session_id: str, kv: dict[str, str]):
        """Commit the session to storage.
        :param session_id: id of the session object.
        :param kv: dictionary of string to json string values, representing the underlying storage of the session.
        """
        pass


_runloop_delegates = None


def register_delegate(delegate: Delegate):
    """Register a delegate to the runloop system registry.
    :param delegate: the delegate to register.
    """
    global _runloop_delegates
    _runloop_delegates = delegate
