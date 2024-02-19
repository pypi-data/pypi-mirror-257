from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Ace(_message.Message):
    __slots__ = ["_id", "deny", "rights"]
    DENY_FIELD_NUMBER: _ClassVar[int]
    RIGHTS_FIELD_NUMBER: _ClassVar[int]
    _ID_FIELD_NUMBER: _ClassVar[int]
    _id: str
    deny: bool
    rights: int
    def __init__(self, _id: _Optional[str] = ..., deny: bool = ..., rights: _Optional[int] = ...) -> None: ...
