from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UnWatchRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UnWatchResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class WatchEvent(_message.Message):
    __slots__ = ["document", "id", "operation"]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    document: str
    id: str
    operation: str
    def __init__(self, id: _Optional[str] = ..., operation: _Optional[str] = ..., document: _Optional[str] = ...) -> None: ...

class WatchRequest(_message.Message):
    __slots__ = ["collectionname", "paths"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    PATHS_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    paths: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, collectionname: _Optional[str] = ..., paths: _Optional[_Iterable[str]] = ...) -> None: ...

class WatchResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...
